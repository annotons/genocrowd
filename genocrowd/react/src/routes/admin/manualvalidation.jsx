import React, { Component } from 'react'
import axios from 'axios'
import { FormGroup, CustomInput, Row, Button } from 'reactstrap'
import BootstrapTable from "react-bootstrap-table-next"
import paginationFactory from "react-bootstrap-table2-paginator";
import cellEditFactory from "react-bootstrap-table2-editor"
import update from 'react-addons-update'
import { Redirect } from 'react-router'
import PropTypes from 'prop-types'
import Iframe from 'react-iframe'

export default class Validation extends Component {
	constructor (props) {
		super(props)
		this.state = ({
			category: 1,
			url: "",
			finished: false,
			gene: "",
			answers: [],
	})
		this.setvalidated = this.setvalidated.bind(this)
		this.handleChangeValidated = this.handleChangeValidated.bind(this)
	}


	setvalidated(event) {
		let gene_id = this.state.gene['_id'];
		let newstatus = false;
		console.log(gene_id)
		
		if (event.target.value == false) {
			newstatus = true;
		}

		let requestUrl = 'api/data/setvalidated';
		let data = {
			'gene': gene_id,
			'newstatus': newstatus,
		}
		axios
			.post(requestUrl, data, {
				baseURL: this.props.config.proxyPath,
				cancelToken: new axios.CancelToken((c) => {
					this.cancelRequest = c;
				}),
			})
			.then((response) => {
				console.log(requestUrl, response.data);
				this.setState({
					error: response.data.error,
					errorMessage : response.data.errorMessage,
					success: !response.data.error,
				})
			})

		//Call level_up
		let annotator = this.state.gene['annotator'];
		let infos = {
			'annotator': annotator,
		}
		let requestUrl_levelup = '/api/auth/levelup';
		axios
			.post(requestUrl_levelup, infos, {
				baseURL: this.props.config.proxyPath,
				cancelToken: new axios.CancelToken((c) => {
					this.cancelRequest = c;
				}),
			})
			.then((response_levelup) => {
				console.log(requestUrl_levelup, response_levelup.data)
			})
	}


	handleChangeValidated(event){
		let geneT = event.target.getAttribute("gene");
	    console.log('Gene_id', geneT)
	    let index = this.state.answers.findIndex((gene) => gene._id == geneT);

	    let newstatus = false;
	    console.log(event.target.value)
	    if (event.target.value == 'false') {
	    	newstatus = true;

		    //Call level_up when gene set to validated
			let annotator = event.target.getAttribute('annotator');
			console.log('Annotator', annotator)
			let infos = {
				'annotator': annotator,
			}
			let requestUrl_levelup = '/api/auth/levelup';
			axios
				.post(requestUrl_levelup, infos, {
					baseURL: this.props.config.proxyPath,
					cancelToken: new axios.CancelToken((c) => {
						this.cancelRequest = c;
					}),
				})
				.then((response_levelup) => {
					console.log(requestUrl_levelup, response_levelup.data)
				})
	    }
	    console.log('newstatus', newstatus)
	    let requestUrl = "/api/data/setvalidated";
	    let data = {
	      gene: geneT,
	      newstatus: newstatus,
	    };

	    axios
	      .post(requestUrl, data, {
	        baseURL: this.props.config.proxyPath,
	        cancelToken: new axios.CancelToken((c) => {
	          this.cancelRequest = c;
	        }),
	      })
	      .then((response) => {
	        console.log(requestUrl, response.data);
	        console.log(this.state.answers[index])
	        this.setState({
	          error: response.data.error,
	          errorMessage: response.data.errorMessage,
	          success: !response.data.error,
	          answers: update(this.state.answers, {
	            [index]: { isValidated: { $set: newstatus } },
	          }),
	        });
	        console.log(this.state.answers[index])

	      });
  	}


	componentDidMount () {
		console.log(this.state.url)
		if (!this.props.config.user) {
			axios.post('/api/auth/check')
			.then(Response => {
				console.log(Response)
				this.props.setStateNavbar({
					config: update(this.props.config,{
						user: {$set: Response.data},
						logged: {$set: !Response.data.error}
					})
				})
			})
			
		}
		
		axios.get('/api/apollo/validation')
			.then(Response => {
				console.log(Response)
				this.setState({
					url: Response.data.url,
					gene : Response.data.gene,
				})
			})
		
		let requestUrl='api/data/getallanswers'
		axios
			.get(requestUrl, {
				baseURL: this.props.config.proxyPath,
				cancelToken: new axios.CancelToken((c) => {
					this.cancelRequest = c;
				}),
			})
			.then((response) => {
				console.log(requestUrl, response.data);
				this.setState({
					error: response.data.error,
					errorMessage: response.data.errorMessage,
					answers: response.data.answer
				})
			})

	}



	render () {
		let html = <Redirect to="/dashboard" />
		let columns = [
			{
				editable: false,
				datafield: "chromosome",
				text: "Chromosome",
				sort: true,
			},
			{
				editable: false,
				dataField: "_id",
				text: "Gene",
				sort: true,
			},
			{
				editable: false,
				dataField: "annotator",
				text: "Annotator",
				sort: "true",
			},
			{
				editable: false,
				dataField: "isAnnotable",
				text: "Annotable",
				sort: true,
			},
			{
				editable: false,
				dataField: "isValidated",
				text: "Validated",
				sort: true,
				formatter: (cell, row) => {
					return (
						<FormGroup>
							<div>
								<CustomInput
									type="switch"
									gene={row._id}
									annotator={row.annotator}
									id={"set-validated-" + row.id}
									name="isValidatd"
									onChange={this.handleChangeValidated}
									label="Validated"
									checked={cell}
									value={cell}
								/>
							</div>
						</FormGroup>
					);
				},
			},
		]

		if (this.state.finished === false) {
			html =  (
				<div className="annotator">
				<h2>Manual Validation</h2>
					<br/>
					<Row>
							<Iframe url={this.state.url}
								width="100%"
								height="700px"
								display="inline"
								position="relative"/>
					</Row>
					<Row>
						<Button color="success" onClick={this.setvalidated}>Validate Annotation</Button>
					</Row>
					<Row>
						<BootstrapTable
							classes="geno-table"
							wrapperClasses="geno-table-wrapper"
							bootstrap4
							keyField="_id"
							data={this.state.answers}
							columns={columns}
							pagination={paginationFactory()}
							cellEdit={cellEditFactory({
								mode: "click",
								autoSelectText: true,
							})}
						/>
					</Row>
				</div>
		)
		}
		
		return html
	}
}


Validation.propTypes = {
	waitForStart: PropTypes.bool,
	config: PropTypes.object,
	setStateNavbar: PropTypes.func
}

