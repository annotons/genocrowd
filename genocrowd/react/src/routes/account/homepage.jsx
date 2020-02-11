import React, { Component } from 'react'
import axios from 'axios'
import { Alert, Button, InputGroupAddon, Input, InputGroup } from 'reactstrap'
import { Redirect } from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'

export default class Homepage extends Component {
  constructor (props) {
    super(props)
  }

  render () {
    return (
      <div className="container">
        <h2> VOUS ETES CONNECTÉ</h2>
      </div>
    )
  }
}
