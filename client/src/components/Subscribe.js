import React from 'react'

class App extends React.Component {
    constructor () {
        super()
        this.state = {}
        }        

    constructor(props) {
        super(props);

        this.state = {
            link: null,
            title: null,
            benefactor: null,
            institution: null,
            faculty: null,
            value: null,
            isRural: null,
            gender: null,
            isLGBT: null,
            isIndigenous: null,
            hardship: null,
            minATAR: null, 
            notes: null 
        };
    }

    componentDidMount() {
        // Simple POST request with a JSON body using fetch
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: 'johnsmith@gmail.com', number: '04930001111', })
        };
        fetch('https://localhost:3000/subscribe', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({ 
                link: null,
                title: null,
                benefactor: null,
                institution: null,
                faculty: null,
                value: null,
                isRural: null,
                gender: null,
                isLGBT: null,
                isIndigenous: null,
                hardship: null,
                minATAR: null, 
                notes: null  
            }));
    }

    render() {
        var json = JSON.parse(data);

        return (
            <div className="card text-center m-3">
                <h5 className="card-header">Simple POST Request</h5>
                <div className="card-body">
                    link: json.link
                    title: json.title,
                    benefactor: json.benefactor,
                    institution: json.institution,
                    faculty: json.faculty,
                    value: json.value,
                    isRural: json.isRural,
                    gender: json.gender,
                    isLGBT: json.isLGBT,
                    isIndigenous: json.isIndigenous,
                    hardship: json.hardship,
                    minATAR: json.minATAR, 
                    notes: json.notes  
                </div>
            </div>
        );
    }
}
   
export { PostRequest }; 


//React.render(<App />, document.getElementById('root'))