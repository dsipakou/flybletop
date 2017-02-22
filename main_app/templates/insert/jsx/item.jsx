import React from 'react';
import { Link } from 'react-router';

class Item extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="col-md-6 col-sm-6 col-xs-12 col-lg-4 catalog-item" >
                <div className="panel">
                    <Link to={`/insert/${this.props.slug}`}>
                        <div className="panel-heading">
                            <img src={this.props.imgsrc} />
                        </div>
                        <div className="panel-heading">
                            <h2 className="panel-title text-info">{this.props.name}</h2>
                        </div>
                    </Link>
                    <div className="panel-body">
                        <p>{this.props.desc}</p>
                        <p><strong>{this.props.price}</strong> <span>$</span></p>
                    </div>
                </div>
            </div>
        )
    }
}

export default Item;