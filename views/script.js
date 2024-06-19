
function ListPost() {

}

function App() {
    return (
        <div className='wrapper'>
            <input type='file' multiple />
        </div>
    )
}


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />)