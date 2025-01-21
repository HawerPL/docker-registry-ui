import logging
import requests as req
from flask_babel import _

from flask import Blueprint, render_template, session, json, flash, redirect, url_for, current_app
from flask_login import login_required
from datetime import datetime


bp = Blueprint('registry', __name__)


@bp.route("/")
@login_required
def registry_explorer():

    special_registry_key = ''
    registries = current_app.config['REGISTRIES']

    authorized_registries = []

    for registry in registries:
        if session.get('registry_url') == registry.url:
            authorized_registries.append(registry)
            registry.repositories = get_repositories(registry)
        if session.get('is_super_user' or not current_app.config['ENABLED_AUTH']):
            authorized_registries.append(registry)
            registry.repositories = get_repositories(registry)

    return render_template("registry-explorer.html", registries=authorized_registries,
                           get_repositories=get_repositories, enable_count_tags=current_app.config['COUNT_TAGS'],
                           count_repository_tags=count_repository_tags,
                           url_for_logged_registry=session.get('registry_url'),
                           special_registry_key=special_registry_key)


@bp.context_processor
def inject_custom_variables():
    return dict(app_name=current_app.config['APP_NAME'])


def get_registry(registry_name):
    return next((reg for reg in current_app.config['REGISTRIES'] if reg.name == registry_name), None)


@bp.route("/<registry_name>/<repository>/tags")
@login_required
def repository_explorer(registry_name, repository):

    registry = get_registry(registry_name)

    tags = get_tags(repository, registry)

    if tags is not None:
        tags = sorted(tags)

    if current_app.config['MINIMAL_REPOSITORY_INFO']:
        sorted_images = [{"name": repository, "tag": value} for value in tags]
    else:
        sorted_images = get_images_info(tags, repository, registry)

    return render_template("repository-explorer.html", registry=registry, repository=repository,
                           images=sorted_images, minimal_info=current_app.config['MINIMAL_REPOSITORY_INFO'])


@bp.route("/<registry_name>/<repository>/<image_tag>")
@login_required
def image_explorer(image_tag, registry_name, repository):
    registry = get_registry(registry_name)

    # image = get_image_details_prettyjws(repository, registry, image_tag)
    manifest = get_image_manifest(repository, registry, image_tag,
                                  "application/vnd.docker.distribution.manifest.list.v2+json")
    manifest.update(get_image_manifest(repository, registry, image_tag,
                                       "application/vnd.docker.distribution.manifest.v2+json"))

    v1_compatibility = json.loads(manifest['history'][0]['v1Compatibility'])

    v1_compatibility['created'] = docker_date_to_datetime(v1_compatibility['created'])

    return render_template("image-explorer.html", repository=repository, image=manifest,
                           v1Compatibility=v1_compatibility, registry=registry, enable_edit_tag=current_app.config['ENABLE_EDIT_TAG'])


@bp.route("/<registry_name>/<repository>/delete/<tag_digest>")
@login_required
def delete_tag(registry_name, repository, tag_digest):
    registry = get_registry(registry_name)
    if registry.isDeletable:
        delete_tag_in_registry(registry, repository, tag_digest)
    else:
        flash("Tag removal is disabled", 'info')
    tags = get_tags(repository, registry)
    images = get_images_info(tags, repository, registry)
    return render_template("repository-explorer.html", registry=registry, repository=repository,
                           images=images)


def delete_tag_in_registry(registry, repository, tag_digest):
    try:
        response = req.delete(registry.url + "/v2/" + repository + "/manifests/" + tag_digest,
                              auth=(registry.login, registry.password), verify=False)
        if response.status_code == 202:
            flash("Success deleting a tag", 'success')
        else:
            flash("Error deleting a tag", 'danger')
    except Exception as e:
        flash("Error deleting a tag", 'danger')
        logging.error(e)


@bp.route("/<registry_name>/<repository>/delete")
@login_required
def delete_tags(registry_name, repository):
    registry = get_registry(registry_name)

    tags = get_tags(repository, registry)
    images = get_images_info(tags, repository, registry)

    if registry.isDeletable:
        for image in images:
            delete_tag_in_registry(registry, repository, image['tag_digest'])
    else:
        flash("Tag removal is disabled", 'info')

    return redirect(url_for('registry.registry_explorer'))


def get_repositories(registry):
    url = registry.url
    try:
        response = req.get(url + f"/v2/_catalog?n={current_app.config['PAGINATION_FOR_REQUEST_CATALOG']}",
                           auth=(registry.login, registry.password), verify=False).json()['repositories']
    except Exception as e:
        response = []
        logging.error(e)
    return response


def get_tags(repository, registry):
    url = registry.url
    try:
        response = req.get(url + "/v2/" + repository +
                           f"/tags/list?n={current_app.config['PAGINATION_FOR_REQUEST_TAGS_LIST']}",
                           auth=(registry.login, registry.password), verify=False).json()['tags']
        logging.info(f"Pobrano tagi dla {repository} z {registry.name}")
    except Exception as e:
        response = []
        logging.error(e)
    return response


def get_images_info(tags, repository, registry):
    images = []
    if tags is not None:
        for tag in tags:
            manifest = get_image_manifest(repository, registry, tag,
                                          "application/vnd.docker.distribution.manifest.list.v2+json")
            manifest.update(get_image_manifest(repository, registry, tag,
                                               "application/vnd.docker.distribution.manifest.v2+json"))
            layers = manifest['layers']
            manifest['sum_size'] = sum(layer['size'] for layer in layers)
            images.append(manifest)
    return images


def get_image_details_prettyjws(repository, registry, tag):
    url = registry.url
    details = {}
    try:
        response = req.get(url + "/v2/" + repository + "/manifests/" + tag,
                           auth=(registry.login, registry.password), verify=False)

        details = response.json()
        details['DockerContentDigest'] = response.headers['Docker-Content-Digest']

        logging.info(f"Pobrano details dla {repository} {tag} z {registry.name}")
    except Exception as e:
        details = {}
        logging.error(e)
    return details


def get_image_manifest(repository, registry, tag, application_header):
    url = registry.url
    details = {}
    headers = {'Accept': f'{application_header}'}
    try:
        response = req.get(url + "/v2/" + repository + "/manifests/" + tag,
                           auth=(registry.login, registry.password), verify=False, headers=headers)

        details = response.json()
        details['tag_digest'] = response.headers['Docker-Content-Digest']

        logging.info(f"Pobrano details dla {repository} {tag} z {registry.name}")
    except Exception as e:
        logging.error(e)
    return details


def count_repository_tags(registry, repository):
    try:
        response = req.get(registry.url + "/v2/" + repository + "/tags/list", auth=(registry.login, registry.password),
                           verify=False)
        if response.status_code == 200:
            list_of_tags = response.json()['tags']
            if list_of_tags is None:
                return 0
            else:
                return len(list_of_tags)
        else:
            return "-1"
    except Exception as e:
        logging.error(e)


def get_registry_by_url(registry_url):
    registry = next((registry for registry in current_app.config['REGISTRIES'] if registry_url == registry.url), None)
    return registry


def delete_repository(registry, repository):
    if not registry.is_deletable:
        for tag in registry.tags:
            delete_tag(registry, repository, tag)
        return 1
    else:
        return 0


def docker_date_to_datetime(docker_date):
    docker_data_format = '%Y-%m-%dT%H:%M:%S.%f'
    data_string = docker_date
    microseconds = int(data_string.split(".")[1][:6])
    data_string = data_string.replace(data_string.split(".")[1], str(microseconds).zfill(6))
    new_format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(data_string, docker_data_format).strftime(new_format)

