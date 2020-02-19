import React, { Component, createContext } from 'react'
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom'
import axios from 'axios'

import About from './routes/about/about'
import GenocrowdNavbar from './navbar'
import GenocrowdFooter from './footer'

import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import Welcome from './routes/welcome/welcome'
import Signup from './routes/login/signup'
import Login from './routes/login/login'
import Dashboard from './routes/account/dashboard'
export default class Routes extends Component {

  constructor (props) {
    super(props)
    this.state = {
      waiting: false,
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

  render () {

    let redirectRoot

    if (document.getElementById('redirect').getAttribute('redirect') == "/") {
      redirectRoot = <Redirect to="/" />
    }


    return (
      <Router basename={this.state.config.proxyPath}>
        <div>
          {redirectRoot}
          <GenocrowdNavbar waitForStart={this.state.waiting} config={this.state.config} />
          <Switch>
            <Route path="/" exact component={() => (<Welcome />)} />
            <Route path="/signup" exact component={() => (<Signup config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/login" exact component={() => (<Login config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/dashboard" exact component={() => (<Dashboard config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />
            <Route path="/about" exact component={() => (<About config={this.state.config} waitForStart={this.state.waiting} setStateNavbar={p => this.setState(p)} />)} />


          </Switch>
          <br />
          <br />
          <GenocrowdFooter config={this.state.config} />
        </div>
      </Router>
    )
  }
}
