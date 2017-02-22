import React from 'react';
import Grid from './grid.jsx'
import Details from './details.jsx'

import { render } from 'react-dom'
import { Router, Route, Link, browserHistory } from 'react-router'


$(document).ready(function() {
    render((
        <Router history={browserHistory}>
            <Route path="/insert" component={Grid} />
            <Route path="/insert/:slug" component={Details} />
        </Router>
    ), document.getElementById('insert_component'))
});
