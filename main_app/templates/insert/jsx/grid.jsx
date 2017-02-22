import Item from './item.jsx';
import React from 'react';
import $ from 'jquery';

import Spinner from 'react-spinkit';

class Grid extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            items: [],
            loaded: false
        }
    }

    componentDidMount() {
        this.loadItems();
    }

    async loadItems() {
        this.setState({
            items: await fetch("/api/v1/product/?type=1").then(response => response.json())
        })
        this.setState({
            loaded: true
        })
    }

    eachItem(item, i) {
        return (<Item slug={item.slug} imgsrc={item.base_image} name={item.name} desc={item.desc}
                                      price={item.price} key={i} />)
    }

    render() {
        if (this.state.loaded) {
            return(
                <div className="row">
                {
                    this.state.items.map(this.eachItem)
                }
                </div>
            );
        } else {
            return(
                <div className="loading">
                    <Spinner spinnerName="cube-grid" />
                </div>
            );
        }
    }
}

export default Grid
