import React from 'react'

class Details extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            details: null
        }
    }

    componentDidmount() {
        this.loadDetails();
        console.log(this.state.details)
    }

    async loadDetails() {
        console.log("asfasfasfdfa")
        this.setState({
            details: await fetch("/api/v1/details?slug=caverna").then(response => response.json())
        })
    }


    render() {
        return (
            <h2>It works! {this.props.params.slug} {this.state.details.name}</h2>
        )
    }
}

export default Details;