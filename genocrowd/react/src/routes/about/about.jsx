import React, { Component } from 'react'
import axios from 'axios'
import { Alert, Button, InputGroupAddon, Input, InputGroup } from 'reactstrap'
import { Redirect } from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'

export default class About extends Component {
  constructor (props) {
    super(props)
  }

  render () {
    return (
      <div className="container">
        <h2>About</h2>
        <hr />
        <h4>What is Genocrowd?</h4>
        <p>
          Genocrowd is...
        </p>
        <h4>Usefull links</h4>
        <p>
            <a target="_newtab" rel="noopener noreferrer" href="https://genocrowd.readthedocs.io">Docs</a>
        </p>
        <p>
            <a target="_newtab" rel="noopener noreferrer" href="https://github.com/annotons/genocrowd">Github repository</a>
        </p>
        <h4>Need help?</h4>
        <p>
          Use <a target="_newtab" rel="noopener noreferrer" href="https://github.com/annotons/genocrowd/issues">Github issues</a> to report a bug, get help or request for a new feature.
        </p>
      </div>
    )
  }
}
