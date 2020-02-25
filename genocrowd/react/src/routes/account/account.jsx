import React, { Component } from 'react'
import axios from 'axios'
import { Button, Form, FormGroup, Label, Input, Alert, Col } from 'reactstrap'
import { Redirect } from 'react-router'
import { Link } from 'react-router-dom'
import UpdateProfile from './update_profile'
import UpdatePassword from './update_password'
import DeleteAccount from './delete_account'

import PropTypes from 'prop-types'

export default class Account extends Component {
  constructor (props) {
    super(props)
    this.state = { isLoading: true,
      error: false,
      errorMessage: [],
    }
  }
  
  handleRemoveAccount(event) {

  }
  render () {
    let html = <Redirect to="/" />
    if (this.props.config.logged) {
    html = (
      <div className="container">
        <UpdateProfile config={this.props.config} setStateNavbar={this.props.setStateNavbar} />
        <hr />
        <UpdatePassword config={this.props.config} setStateNavbar={this.props.setStateNavbar} />
        <hr />
        <Link to="/delete"> <Button color="danger">Delete Account</Button></Link>
      </div>
    )
  }
  return html
}
}
Account.propTypes = {
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}
