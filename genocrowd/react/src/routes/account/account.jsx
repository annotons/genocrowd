import React, { Component } from 'react'

import { Button } from 'reactstrap'
import { Redirect } from 'react-router'
import { Link } from 'react-router-dom'
import UpdateProfile from './update_profile'
import UpdatePassword from './update_password'

import PropTypes from 'prop-types'

export default class Account extends Component {
  constructor (props) {
    super(props)
    this.state = { isLoading: true,
      error: false,
      errorMessage: [],
    }
  }
  
  handleRemoveAccount() {

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
