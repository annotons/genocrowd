import React, { Component } from 'react'
import axios from 'axios'
import { Button, Form, FormGroup, Label, Input, Alert } from 'reactstrap'
import { Redirect } from 'react-router'
import { Link } from 'react-router-dom'
import update from 'immutability-helper'
import ErrorDiv from '../error/error'
import PropTypes from 'prop-types'

export default class Signup extends Component {
  constructor (props) {
    super(props)
    this.state = { isLoading: true,
      error: false,
      errorMessage: '',
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      password: '',
      passwordconf: '',
      usernameFirstChar: '',
      usernameLastChars: ''
    }
    this.handleChange = this.handleChange.bind(this)
    this.handleChangeFirst_name = this.handleChangeFirst_name.bind(this)
    this.handleChangeLname = this.handleChangeLname.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.cancelRequest
  }

  handleChangeFirst_name (event) {
    this.setState({
      username: event.target.value.charAt(0).toLowerCase(),
      first_name: event.target.value
    })
  }

  handleChangeLname (event) {
    this.setState({
      username: this.state.first_name.charAt(0).toLowerCase() + event.target.value.toLowerCase(),
      last_name: event.target.value
    })
  }

  handleChange (event) {
    this.setState({
      [event.target.id]: event.target.value
    })
  }

  validateEmail (email) {
    let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return re.test(String(email).toLowerCase())
  }

  validateForm () {
    return (
      
      this.validateEmail(this.state.email) &&
      this.state.username.length > 0 &&
      this.state.password.length > 0 &&
      this.state.passwordconf == this.state.password
    )
  }

  handleSubmit (event) {
    let requestUrl = '/api/auth/signup'
    let data = {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password,
      passwordconf: this.state.passwordconf
    }

    axios.post(requestUrl, data, { baseURL: this.props.config.proxyPath, cancelToken: new axios.CancelToken((c) => { this.cancelRequest = c }) })
      .then(response => {
        console.log(requestUrl, response.data)
        this.setState({
          isLoading: false,
          error: response.data.error,
          errorMessage: response.data.errorMessage,
          status: response.status,
          Redirect: true
        })
        if (!this.state.error) {
          this.props.setStateNavbar({
            config: update(this.props.config,{
              user: {$set: response.data.user},
              logged: {$set: !response.data.error}
            })
          })
        }
      })
      .catch(error => {
        console.log(error)
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status: error.response.status,
          success: !response.data.error,
          username: '',
          email: '',
          password: '',
          passwordconf: ''
        })
      })
    event.preventDefault()
  }

  componentWillUnmount () {
    if (this.cancelRequest) {
      this.cancelRequest()
    }
  }

  render () {
    let html = <Redirect to="/login" />
    if (!this.props.config.logged) {
      html = (
        <div className="container">
          <h2>Signup</h2>
          <hr />
          <div className="col-md-4">
            <Form onSubmit={this.handleSubmit}>
              <FormGroup>
                <Label for="email">Email</Label>
                <Input type="email" name="email" id="email" placeholder="email" value={this.state.email} onChange={this.handleChange} />
              </FormGroup>
              <FormGroup>
                <Label for="username">Username</Label>
                <Input type="text" name="username" id="username" placeholder="username" value={this.state.username} onChange={this.handleChange} />
              </FormGroup>
              <FormGroup>
                <Label for="password">Password</Label>
                <Input type="password" name="password" id="password" placeholder="password" value={this.state.password} onChange={this.handleChange} />
              </FormGroup>
              <FormGroup>
                <Label for="passwordconf">Password (confirmation)</Label>
                <Input type="password" name="passwordconf" id="passwordconf" placeholder="password (confirmation)" value={this.state.passwordconf} onChange={this.handleChange} />
              </FormGroup>
              <Button disabled={!this.validateForm()}>Signup</Button>
              <p>(Or <Link to="/login"> login</Link>)</p>
            </Form>
            <ErrorDiv status={this.state.status} error={this.state.error} errorMessage={this.state.errorMessage} />
          </div>
        </div>
      )
    }
    return html
  }
}

Signup.propTypes = {
  setStateNavbar: PropTypes.func,
  config: PropTypes.object
}
