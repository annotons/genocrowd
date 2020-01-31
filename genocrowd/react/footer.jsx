import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { Collapse, Navbar, NavbarBrand, Nav, NavItem } from 'reactstrap'
import PropTypes from 'prop-types'

export default class GenocrowdFooter extends Component {
  constructor (props) {
    super(props)
  }

  render () {
      let commitLink
      if (this.props.config.commit) {
        commitLink = (<>- <a href={this.props.config.gitUrl + "/commit/" + this.props.config.commit}>{this.props.config.commit}</a></>)
      }
    return (
      <footer className="footer footer-content">
        <div className="container">
          <div className="footer-left">
            Genocrowd {this.props.config.version} {commitLink}
          </div>
          <div className="footer-right">
            {this.props.config.footerMessage}
          </div>
        </div>
      </footer>
    )
  }
}

GenocrowdFooter.propTypes = {
  config: PropTypes.object
}
