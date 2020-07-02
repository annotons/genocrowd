import React, { Component } from "react";
import {
  Button,
  CardBody,
  Row,
  Container,
  Col,
  Card,
  CardTitle,
  CardSubtitle,
  CardImg,
  CardHeader,
  Progress,
  ListGroup,
  ListGroupItem,
} from "reactstrap";
import PropTypes from "prop-types";
import Identicon from "react-identicons";
import { Redirect } from "react-router";

export default class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      start: false,
    };
    this.setStart = this.setStart.bind(this);
  }

  setStart() {
    this.setState({ start: true });
  }
  render() {
    let html = <Redirect to="/annotator" />;
    if (this.state.start === false) {
      html = (
        <Container>
          <Row>
            <Col xs="auto">
              <Row>
                <Card className="dashboard-cards">
                  <br></br>
                  <CardTitle tag="h3">
                    {this.props.config.user.username}
                  </CardTitle>
                  <CardSubtitle>GroupName</CardSubtitle>
                  <CardBody>
                    <br></br>
                    <Container></Container>
                    <Progress value={2 * 5}></Progress>
                    <br></br>
                    <Identicon
                      size={100}
                      string={this.props.config.user.username}
                    />
                  </CardBody>
                </Card>
              </Row>
              <Row>
                <Card className="dashboard-cards">
                  <ListGroup>
                    <ListGroupItem>gene</ListGroupItem>
                    <ListGroupItem>gene</ListGroupItem>
                    <ListGroupItem>gene</ListGroupItem>
                    <ListGroupItem>gene</ListGroupItem>
                  </ListGroup>
                </Card>
              </Row>
            </Col>
            
            <Col>
              <Col>
                <Row>
                  <Card body outline className="dashboard-cards">
                    <CardTitle>Project progress</CardTitle>
                    <CardImg
                      size="130%"
                      src="../../../../static/logo/fauxcamembert.png"
                    ></CardImg>
                    <hr></hr>
                    <Button success>Get Started</Button>
                  </Card>
                </Row>
              </Col>
              <Col>
                <Row>
                  <Card className="dashboard-statcards">
                    <CardHeader>Annotated genes</CardHeader>
                    <CardBody>1000</CardBody>
                  </Card>
                </Row>
                <Row>
                  <Card className="dashboard-statcards">
                    <CardHeader>Number of annotators</CardHeader>
                    <CardBody>150</CardBody>
                  </Card>
                </Row>
                <Row>
                  <Card className="dashboard-statcards">
                    <CardHeader>Number of groups</CardHeader>
                    <CardBody>15</CardBody>
                  </Card>
                </Row>
              </Col>
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
