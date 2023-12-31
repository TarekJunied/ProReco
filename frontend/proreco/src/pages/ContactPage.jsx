import { Form, TextArea } from 'semantic-ui-react';
import Swal from 'sweetalert2';

import backgroundImage from '../assets/background.png';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import emailjs from 'emailjs-com';
import ChooseLayout from "../layout/ChooseLayout"
import "../index.css"
let SERVICE_ID = "service_w3ucaxq";
let TEMPLATE_ID = "template_5e1bu2z"
let PUBLIC_KEY = "G3GpzYf315YbbJ3_J";


const labelStyle = {
    color: "white",
    fontSize: "40px"
}
const formStyle = {
    width: "70vw",
    margin: "auto",
    marginBottom: "200px",
    textAlign: "center",
    paddingBottom: "300px",
    flexDirection: "column",
    justifyContent: "center"
};
const inputStyle = {
    width: "100%",
    marginBottom: "10px",
    height: "7vh",
    fontSize: "30px"
};
const textAreaStyle = {
    width: "100%",
    marginBottom: "70vh",
    minHeight: "70vh",
    paddingBottom: "70vh"
}
//confirmButtonColor: '#BF3604',

const imageUrl = "https://proreco.co/cuteIcon.png"
const ContactPage = () => {
    const handleOnSubmit = (e) => {
        Swal.fire({
            title: 'Message Sent Successfully',
            confirmButtonColor: '#BF3604',
            imageUrl: imageUrl,
            imageWidth: 250,
            imageHeight: 250,
            imageAlt: 'Custom image',
            animation: true

        }).then((result) => {
            if (result.isDismissed) {
                console.error('Swal.fire dismissed.');
            } else if (result.isConfirmed) {
                console.log('Swal.fire confirmed.');
            } else if (result.isDenied) {
                console.warn('Swal.fire denied.');
            }
        }).catch((error) => {
            console.error('Swal.fire error:', error);
        });



        e.preventDefault();

        e.target.reset()
    };

    return (
        <ChooseLayout>

            <div style={formStyle}>
                <Form onSubmit={handleOnSubmit}>
                    <Form.Field name="name" >

                        <label style={labelStyle}>Name</label>
                        <input name="name" placeholder="Your Name" style={inputStyle} />
                    </Form.Field>
                    <Form.Field name="email" >
                        <label style={labelStyle}>Email</label>
                        <input name="email" type="email" placeholder="Your Email" style={inputStyle} />
                    </Form.Field>
                    <Form.Field style={inputStyle}>
                        <label style={labelStyle}>Message</label>
                        <TextArea name="message" placeholder="Your Message" style={textAreaStyle} />
                    </Form.Field>
                    <button style={{
                        color: "white",
                        background: `linear-gradient(157.81deg,
                            #FFA000 -43.27%,
                            #FF8C00 -21.24%,
                            #FF7700 12.19%,
                            #FF6300 29.82%,
                            #FF4F00 51.94%,
                            #BF3604 90.29%)`,
                        width: "17vw",
                        marginTop: "90vh",
                        height: "10vh",
                        fontSize: "3vw", borderRadius: "10px"


                    }} >Submit</button>


                </Form>
            </div>

        </ChooseLayout>
    );
};

export default ContactPage;
