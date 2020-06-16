import React, { Component } from 'react'
import axios from 'axios'
import { Jumbotron, Button } from 'reactstrap'
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
      <div className='container'>
        <Jumbotron className='welcome-jumbotron'>
          <h1 className='welcome-h1'>Welcome to Genocrowd!</h1>
          <p className='welcome-p'>This is a Web-based Annotation tool designed towards citizen science</p>
          <p className='welcome-p'> <Button variant="primary">Jump in!</Button></p>
        </Jumbotron>
        {/* <Card>
          <CardImg top className="img-fluid" src="../../../../static/logo/dna.jpg"></CardImg>

        </Card> */}
      </div>
    )
  }
}


Welcome.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}

