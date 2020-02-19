import React, { Component } from 'react'
import axios from 'axios'
import { Button, Form, FormGroup, Label, Input, Alert, Navbar } from 'reactstrap'
import { Redirect} from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'

export default class Dashboard extends Component {
  constructor (props) {
    super(props)
    
    
  }
  
  render () {
    let html = (
    <div className="container">
    <h2> VOUS ETES CONNECTÉ</h2>
    {/* <li><Link to="/logout" className="btn btn-primary">Log Out</Link></li> */}
    </div>
    )
    if(!this.props.config.logged){
        
      return <Redirect to='/login'/>;
    }
    return html
  }
}
Dashboard.propTypes = {
  config: PropTypes.object
}
