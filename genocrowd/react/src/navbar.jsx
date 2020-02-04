import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { Collapse, Navbar, NavbarBrand, Nav, NavItem, Dropdown, DropdownMenu, DropdownToggle, DropdownItem } from 'reactstrap'
import PropTypes from 'prop-types'

export default class GenocrowdNavbar extends Component {
  constructor (props) {
    super(props)
    this.toggle = this.toggle.bind(this)
    this.state = {
      dropdownOpen: false
    }
  }

  toggle () {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen
    })
  }

  render () {
    let links
    let aboutLink

    // if wait is false
    if (!this.props.waitForStart) {
      links = (
        <>
          <NavItem><Link className="nav-link" to="/about"><i className="fas fa-info"></i> About</Link></NavItem>
        </>
      )
    }

    return (
      <div>
        <Navbar color="dark" dark expand="md">
          <div className="container">
            <NavbarBrand href={this.props.config.proxyPath == "/" ? "/" : this.props.config.proxyPath + "/"}>Genocrowd</NavbarBrand>
            <Collapse navbar>
              <Nav className="ml-auto" navbar>
                {links}
              </Nav>
            </Collapse>
          </div>
        </Navbar>
        <br />
      </div>
    )
  }
}

GenocrowdNavbar.propTypes = {
  waitForStart: PropTypes.bool,
  config: PropTypes.object
}
