import { Form, TextArea } from 'semantic-ui-react';
import Swal from 'sweetalert2';

import backgroundImage from '../assets/background.png';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import emailjs from 'emailjs-com';


let SERVICE_ID = "service_w3ucaxq";
let TEMPLATE_ID = "template_5e1bu2z"
let PUBLIC_KEY = "G3GpzYf315YbbJ3_J";

const labelStyle = {
    color: "white",
    fontSize: "40px"
}
const formStyle = {
    width: "70vw",
    margin: "20px auto",
    marginBottom: "200px",
    textAlign: "center",
    paddingBottom: "300px",
    flexDirection: "column",
    justifyContent: "center"
};
const inputStyle = {
    width: "100%",
    marginBottom: "10px",
    height: "10vh",
    fontSize: "30px"
};
const textAreaStyle = {
    width: "100%",
    marginBottom: "70vh",
    minHeight: "70vh",
    paddingBottom: "70vh"
}

const ContactPage = () => {
    const handleOnSubmit = (e) => {
        e.preventDefault();
        emailjs.sendForm(SERVICE_ID, TEMPLATE_ID, e.target, PUBLIC_KEY)
            .then((result) => {
                console.log(result.text);
                Swal.fire({
                    icon: 'success',
                    title: 'Message Sent Successfully'
                })
            }, (error) => {
                console.log(error.text);
                Swal.fire({
                    icon: 'error',
                    title: 'Ooops, something went wrong',
                    text: error.text,
                })
            });
        e.target.reset()
    };

    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "bottom",
            backgroundRepeat: "repeat-y",
            width: "100vw",
            minHeight: "100vh",

        }}>
            <NavBar />

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
                        width: "20vw",
                        marginTop: "90vh",
                        height: "15vh",
                        fontSize: "60px", borderRadius: "10px"


                    }} >Submit</button>


                </Form>
            </div>

            <Footer />
        </div>
    );
};

export default ContactPage;
