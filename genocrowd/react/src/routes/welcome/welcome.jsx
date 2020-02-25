import React, { Component } from 'react'
import axios from 'axios'
import { Alert, Button, InputGroupAddon, Input, InputGroup } from 'reactstrap'
import { Redirect } from 'react-router-dom'
import ErrorDiv from '../error/error'
import WaitingDiv from '../../components/waiting'
import update from 'react-addons-update'
import PropTypes from 'prop-types'
import GenocrowdNavbar from '../../navbar'
export default class Welcome extends Component {
  constructor (props) {
    super(props)
    
  }

  componentDidMount () {

    if (this.props.config.user) {
      
      console.log(this.props.config)
      }
    else {
      axios.post('/api/auth/check')
      .then(Response => {
        this.props.setStateNavbar({
          config: update(this.props.config,{
            user: {$set: Response.data.user},
            logged: {$set: !Response.data.error}
          })
        })

      })
    }
    }
  render () {
    return (
      <div className="container">
        <h2> Welcome to Genocrowd!</h2>
        
        <hr />
        
       
        
      </div>
    )
  }
}


Welcome.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}

