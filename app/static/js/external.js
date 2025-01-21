
const copyButtons = document.querySelectorAll('.copy-btn');

copyButtons.forEach(btn => {
    btn.addEventListener('click', function () {
        let text_to_copy = document.querySelector(btn.getAttribute("data-clipboard-target")).innerHTML
        copyTextToClipboard(text_to_copy.trim())
    })
})

function copyTextToClipboard(text) {
             let textArea = document.createElement("textarea");
             textArea.value = text;
             document.body.appendChild(textArea);
             textArea.select();
             document.execCommand('copy');
             document.body.removeChild(textArea);
         }



