
function ListPost() {

}

function App() {
    return (
        <div className='wrapper'>
            <input type='file' id='file-input' multiple />
        </div>
    )
}


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />)


