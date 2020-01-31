import React, { Component, createContext } from 'react'
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom'
import axios from 'axios'

import Ask from './routes/ask/ask'
import About from './routes/about/about'
import Signup from './routes/login/signup'
import Login from './routes/login/login'
import Logout from './routes/login/logout'
import Account from './routes/account/account'
import Admin from './routes/admin/admin'
import GenocrowdNavbar from './navbar'
import GenocrowdFooter from './footer'

import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'

export default class Routes extends Component {

  constructor (props) {
    super(props)
    this.state = {
      waiting: true,
      error: false,
      errorMessage: null,
      config: {
        proxyPath: document.getElementById('proxy_path').getAttribute('proxy_path'),
        user: {},
        logged: false,
        footerMessage: null,
        version: null,
        commit: null,
        gitUrl: null,
        disableIntegration: null,
        prefix: null,
        namespace: null
      }
    }
    this.cancelRequest
  }

  componentDidMount () {

    let requestUrl = '/api/start'
    axios.get(requestUrl, {baseURL: this.state.config.proxyPath , cancelToken: new axios.CancelToken((c) => { this.cancelRequest = c }) })
      .then(response => {
        console.log(requestUrl, response.data)
        this.setState({
          error: false,
          errorMessage: null,
          config: response.data.config,
          waiting: false
        })
      })
      .catch(error => {
        console.log(error, error.response.data.errorMessage)
        this.setState({
          error: true,
          errorMessage: error.response.data.errorMessage,
          status: error.response.status,
          waiting: false
        })
      })
  }

  render () {

    let redirectRoot

    if (document.getElementById('redirect').getAttribute('redirect') == "/") {
      redirectRoot = <Redirect to="/" />
    }

    let admin = false
    if (this.state.config.user) {
      admin = this.state.config.user.admin
    }


    return (
      <Router basename={this.state.config.proxyPath}>
        <div>
          {redirectRoot}
          <GenocrowdNavbar waitForStart={this.state.waiting} config={this.state.config} />
          <Switch>
            <Route path="/" exact component={() => (<Ask waitForStart={this.state.waiting} config={this.state.config} />)} />
            <Route path="/about" exact component={() => (<About />)} />
            <Route path="/login" exact component={() => (<Login config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/signup" exact component={() => (<Signup config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/logout" exact component={() => (<Logout config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/account" exact component={() => (<Account config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/admin" exact component={() => (<Admin config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
          </Switch>
          <br />
          <br />
          <GenocrowdFooter config={this.state.config} />
        </div>
      </Router>
    )
  }
}
