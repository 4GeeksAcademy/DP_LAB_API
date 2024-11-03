import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Tab, Tabs } from 'react-bootstrap';
import { useReactToPrint } from 'react-to-print';
import "../../styles/customerview.css";

const CustomerView = () => {
    const { customerId } = useParams();
    const [customer, setCustomer] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const componentRef = useRef();

    useEffect(() => {
        const fetchCustomer = async () => {
            try {
                const response = await axios.get(`${process.env.BACKEND_URL}/api/customers/${customerId}`);
                setCustomer(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchCustomer();
    }, [customerId]);

    const handlePrint = useReactToPrint({
        content: () => {
            console.log('Printing...');
            return componentRef.current;
        },
    });

    if (loading) return <p>Un poquillo de paciencia, please!!...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="d-flex justify-content-center align-items-start vh-100 custom-container">
            <div className="container mt-0 justify-content-center" ref={componentRef}>

                <Tabs defaultActiveKey="customer" id="customer-tabs" className="mb-1">
                    <Tab eventKey="customer" title="Cliente" >

                        <div className='d-flex'>
                            <p ><strong>Nº Cliente:</strong> {customer.id}</p>
                            <div className="p-3">
                                <h4 >{customer.first_name} {customer.last_name}</h4>
                            </div>
                            <div className="p-3">
                                <h5 >{customer.billing.company}</h5>
                            </div>


                        </div>
                        <div>
                            <p><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#354278"><path d="M160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm320-280L160-640v400h640v-400L480-440Zm0-80 320-200H160l320 200ZM160-640v-80 480-400Z" /></svg> <a href="mailto:{{customer.email}}">{customer.email}</a></p>
                            <p><svg class xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#354278"><path d="M560-440q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35ZM280-320q-33 0-56.5-23.5T200-400v-320q0-33 23.5-56.5T280-800h560q33 0 56.5 23.5T920-720v320q0 33-23.5 56.5T840-320H280Zm80-80h400q0-33 23.5-56.5T840-480v-160q-33 0-56.5-23.5T760-720H360q0 33-23.5 56.5T280-640v160q33 0 56.5 23.5T360-400Zm440 240H120q-33 0-56.5-23.5T40-240v-440h80v440h680v80ZM280-400v-320 320Z" /></svg>     {customer.role}</p>
                            <p><strong><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#354278"><path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-160v-112q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v112H160Zm80-80h480v-32q0-11-5.5-20T700-306q-54-27-109-40.5T480-360q-56 0-111 13.5T260-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T560-640q0-33-23.5-56.5T480-720q-33 0-56.5 23.5T400-640q0 33 23.5 56.5T480-560Zm0-80Zm0 400Z" /></svg></strong> {customer.username}</p>
                        </div>


                    </Tab>
                    <Tab eventKey="billing" title="Facturación">

                        {customer.billing ? (
                            <div>
                                <p><strong>Company:</strong> {customer.billing.company}</p>
                                <p><strong>Address 1:</strong> {customer.billing.address_1}</p>
                                <p><strong>Address 2:</strong> {customer.billing.address_2}</p>
                                <p><strong>City:</strong> {customer.billing.city}</p>
                                <p><strong>State:</strong> {customer.billing.state}</p>
                                <p><strong>Postcode:</strong> {customer.billing.postcode}</p>
                                <p><strong>Country:</strong> {customer.billing.country}</p>
                                <p><strong>Email:</strong> {customer.billing.email}</p>
                                <p><strong>Phone:</strong> {customer.billing.phone}</p>
                            </div>
                        ) : (
                            <p>No billing information available.</p>
                        )}
                    </Tab>
                    <Tab eventKey="shipping" title="Envío">

                        {customer.shipping ? (
                            <div>
                                <p><strong>Company:</strong> {customer.shipping.company}</p>
                                <p><strong>Address 1:</strong> {customer.shipping.address_1}</p>
                                <p><strong>Address 2:</strong> {customer.shipping.address_2}</p>
                                <p><strong>City:</strong> {customer.shipping.city}</p>
                                <p><strong>State:</strong> {customer.shipping.state}</p>
                                <p><strong>Postcode:</strong> {customer.shipping.postcode}</p>
                                <p><strong>Country:</strong> {customer.shipping.country}</p>
                            </div>
                        ) : (
                            <p>Sin datos de envío</p>
                        )}
                    </Tab>
                </Tabs>
                <button onClick={handlePrint} className="btn btn-custom mb-3">Imprimir</button>

                <h2>Orders</h2>
                {customer.orders && customer.orders.length > 0 ? (
                    <ul>
                        {customer.orders.map(order => (
                            <li key={order.id}>Order Number: {order.number} - Total: {order.total}</li>
                        ))}
                    </ul>
                ) : (
                    <p>No hay pedidos de este cliente.</p>
                )}
            </div>
        </div>
    );
};

export default CustomerView;