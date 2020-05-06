import React, { Component } from "react";
import {
  Button,
  Media,
  CardBody,
  Row,
  Container,
  Col,
  Table,
  Jumbotron,
  Card,
} from "reactstrap";
import PropTypes from "prop-types";
import Identicon from "react-identicons";
import { Redirect } from "react-router";

export default class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      start: false
    }
    this.setStart = this.setStart.bind(this)
  }

  setStart() {
    this.setState({ start: true })
  }
  render() {
    let html = <Redirect to="/annotator" />;
    if (this.state.start === false) {
      html = (
        <Container>
          <Row>
            <Col width={50} xs>
              <Card width={50} body outline color="secondary">
                <Media>
                  <Media left href="#top">
                    <Identicon
                      size={100}
                      string={this.props.config.user.username}
                    />
                  </Media>
                  <Media body>{this.props.config.user.username}</Media>
                </Media>
              </Card>
            </Col>
            <Col width={50} xs>
              <Card body outline color="secondary">
                <CardBody className="text-center tile ">
                  {this.props.config.user.username}
                </CardBody>
              </Card>
            </Col>
          </Row>

          <Row>
            <Jumbotron>
              <Container>
                <h1 className="display-4">Statistics</h1>
                <h2 className="display-5">Number of Annotated genes</h2>
                <p className="lead">57</p>
              </Container>
            </Jumbotron>
          </Row>
          <Row>
            <Col>
              <Table hover>
                <thead>
                  <tr>
                    <th>Twitter feed</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>dude1: Best tool ever #genocrowd</td>
                  </tr>
                  <tr>
                    <td>dude2: The future of annotation tools! #genocrowd</td>
                  </tr>
                  <tr>
                    <td>etc...</td>
                  </tr>
                </tbody>
              </Table>
            </Col>
            <Col>
              <Jumbotron>
                <h1 className="display-3">Hello</h1>
                <p className="lead">You can now Annotate!</p>
                <hr className="my-2" />
                <Button
                  color="success"
                  onClick={this.setStart}
                >
                  Get Started
                </Button>{" "}
              </Jumbotron>
            </Col>
            <Col>
              <Table hover>
                <thead>
                  <tr>
                    <th colSpan="2">Top Annotators</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>1</td>
                    <td>Me</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Myself</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td>I</td>
                  </tr>
                </tbody>
              </Table>
            </Col>
          </Row>
        </Container>
      );
    }
    return html;
    
  }
}
Dashboard.propTypes = {
  config: PropTypes.object,
};
