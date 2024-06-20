const inputFileElm = document.getElementById('input-file');

inputFileElm.addEventListener('change', async event => {

    const files = Object.values(event.target.files);
    const promises = files.map(file => readFileAsJson(file));
    const myData = await Promise.all(promises);
    
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App props={myData} />);
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

function App({ props }) {
    return (
        <div className='wrapper'>
            {
                props.map((listItem, index) => <ListItem props={listItem} key={index} />)
            }
        </div>
    )
}

function ListItem({ props }) {
    return Object.values(props).map((item, index) => {
        return (
            <div className='list-item' key={index}>
                <table>
                    <tr>
                        {
                            item.map((header, headerIndex) => {
                                console.log(header, headerIndex);
                                return <th key={headerIndex}>{header}</th>
                            })
                        }
                    </tr>
                </table>
            </div>
        )
    })
    return (
        <div className='list-item'>
            {
                Object.values(props).map((item, index) => {
                    return (
                        <div className>

                        </div>
                    )
                    // return item.map(value => {
                    //     return (
                    //         <div>

                    //         </div>
                    //     )
                    // })
                })
            }
        </div>
    )
}