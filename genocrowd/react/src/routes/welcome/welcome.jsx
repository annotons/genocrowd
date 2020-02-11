import React, { Component } from 'react'
import axios from 'axios'
import { Alert, Button, InputGroupAddon, Input, InputGroup } from 'reactstrap'
import { Redirect } from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'
export default class Welcome extends Component {
  constructor (props) {
    super(props)
  }

  render () {
    return (
      <div className="container">
        <h2> Welcome to Genocrowd!</h2>
        <hr />
        <h4>
            <p>
                <a target="_newtab" rel="noopener noreferrer" href="./login">LOGIN</a>
            </p>
            <p>
                <a target="_newtab" rel="noopener noreferrer" href="./signup">REGISTER</a>
            </p>
        </h4>
       
        
      </div>
    )
  }
}
