import React, { Component } from 'react'
import axios from 'axios'
import { Card, CardImg } from 'reactstrap'
import update from 'react-addons-update'
import PropTypes from 'prop-types'
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
      <div>
        <h3>Welcome to Genocrowd!</h3>
        <hr/>
        <Card>
          <CardImg top className="img-fluid" src="../../../../static/logo/dna.jpg"></CardImg>

        </Card>
      </div>
    )
  }
}


Welcome.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}

