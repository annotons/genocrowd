import React, { Component } from 'react'
import { Redirect } from 'react-router'
import Users from './usersmanagement'

import PropTypes from 'prop-types'
import SpecificGeneSelection from './specificgeneselection'
import GeneBoard from './geneselector'
export default class Admin extends Component {
  constructor (props) {
    super(props)
    this.state = { isLoading: true,
      error: false,
      errorMessage: [],
    }
  }
  

  render () {
    let html = <Redirect to="/" />
    if (this.props.config.logged) {
    html = (
      <div className="container">
        <Users config={this.props.config} setStateNavbar={this.props.setStateNavbar} />
        <hr />
        <GeneBoard config={this.props.config} setStateNavbar={this.props.setStateNavbar} />
        <SpecificGeneSelection config={this.props.config} setStateNavbar={this.props.setStateNavbar} />
      </div>
    )
  }
  return html
}
}
Admin.propTypes = {
  config: PropTypes.object,
  setStateNavbar: PropTypes.func
}
