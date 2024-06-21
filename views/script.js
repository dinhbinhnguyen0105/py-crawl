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

    return (
        <div className='list-item'>
            {
                Object.values(props).map((browser, browserIndex) => {
                    return <Table props={browser} key ={browserIndex} />
                })
            }
        </div>
    )
}

function Table({props}) {
    return (
        <div className='table'>
            <div className='table-header'>
                <div className='header-no no'>No</div>
                <div className='header-url url'>Link</div>
                <div className='header-description description'>Description</div>
                <div className='header-comment comment'>Comment</div>
                <div className='header-images images'>Images</div>
            </div>
            <div className='table-body'>
                {
                    props.map((row, rowIndex) => {
                        return (
                            <div className='table-row' key={rowIndex}>
                                <div className='cell no'>{row.no}</div>
                                <div className='cell url'>{row.url}</div>
                                <div className='cell description'>{row.description}</div>
                                <div className='cell comment'>{row.comment}</div>
                                <div className='cell images'>{row.images}</div>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}