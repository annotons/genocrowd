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
    let genoLink
    // if wait is false
    if (!this.props.waitForStart) {
      
      genoLink = (
        <NavItem><Link className="nav-link" to="/"><i className="fas fa-play"></i> GenoHome</Link></NavItem>
      )
      links = (
        <>
          <NavItem><Link className="nav-link" to="/about"><i className="fas fa-info"></i> About</Link></NavItem>
          <NavItem><Link className="nav-link" to="/login"><i className="fas fa-sign-in-alt"></i> Login</Link></NavItem>
          <NavItem><Link className="nav-link" to="/signup"><i className="fas fa-sign-in-alt"></i> Sign up</Link></NavItem>

        </>
      )

      if (this.props.config.logged) {
        
        let adminLinks
        console.log(this.props.config.user.isAdmin)
        if (this.props.config.user.isAdmin) {
          adminLinks = (
            <>
            <NavItem><Link className="nav-link" to="/admin"><i className="fas fa-chess-king"></i> Admin</Link></NavItem>
            </>
          )
        }
        let integrationLinks
        if (this.props.config.logged) {
          integrationLinks = (
            <>
            <NavItem><Link className="nav-link" to="/dashboard"><i className="fas fa-home"></i> Dashboard</Link></NavItem>
            
            </>
          )
        }
        links = (
          <>
          {integrationLinks}
          {adminLinks}
          <NavItem><Link className="nav-link" to="/about"><i className="fas fa-info"></i> About</Link></NavItem>
          <NavItem>
            <Dropdown nav isOpen={this.state.dropdownOpen} toggle={this.toggle}>
              <DropdownToggle nav caret>
                <i className="fas fa-user"></i> {this.props.config.user.email} 
                
              </DropdownToggle>
              <DropdownMenu className="bg-dark">
                <DropdownItem className="bg-dark" tag="Link">
                  <Link className="nav-link" to="/account"><i className="fas fa-cog"></i> Account managment</Link>
                </DropdownItem>
                
                <DropdownItem className="bg-dark" divider />
                <DropdownItem className="bg-dark" tag="Link">
                  <Link className="nav-link" to="/logout"><i className="fas fa-sign-out-alt"></i> Logout</Link>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </NavItem>
          </>
        )
      }


      
    }

    return (
      <div>
        <Navbar color="dark" dark expand="md">
          <div className="container">
            <NavbarBrand href={this.props.config.proxyPath == "/" ? "/" : this.props.config.proxyPath + "/"}> <img src="../static/logo/logoGenocrowd.png"width= {120} height={30} mode='fit'/></NavbarBrand>
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
