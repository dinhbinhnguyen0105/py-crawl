const inputFileElm = document.getElementById('input-file');

inputFileElm.addEventListener('change', async event => {

    const files = Object.values(event.target.files);
    const promises = files.map(file => readFileAsJson(file));
    const myData = await Promise.all(promises);
    console.log(myData);

})

function readFileAsJson(file) {
    return new Promise((resolve, reject) => {
        const fileRender = new FileReader();
        fileRender.onload = e => {
            const content = e.target.result;
            const jsonContent = JSON.parse(content);
            resolve(jsonContent);
        }
        fileRender.onerror = () => {
            reject(fileRender.error);
        }
        fileRender.readAsText(file);
    })
}