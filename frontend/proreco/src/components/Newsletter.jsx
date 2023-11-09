import { useState } from "react";
import Button from "./Button";
import "../index.css"
function Newsletter() {
    const [email, setEmail] = useState("");
    const [error, setError] = useState(false);

    const handleChange = (value) => {
        setEmail(value);
        setError(false);
    };

    const handleSubmit = () => {
        const isInvalidEmail = !/^[A-Za-z0-9._%+-]{1,64}@(?:[A-Za-z0-9-]{1,63}\.){1,125}[A-Za-z]{2,63}$/.test(
            email
        );

        if (isInvalidEmail) {
            setError(true);
        } else {
            console.log(email);
        }
    };

    return (
        <div>
            <section>
                <p>Want to learn more about the exciting world of Process Mining ? </p>

                <div className="flex flex-row align-center justify-center">
                    <p className="mr-5 text-white">Join the newsletter </p>
                    <input
                        className={error ? "error" : ""}
                        type="text"
                        placeholder="Enter your favourite email !"
                        value={email}
                        onChange={(e) => handleChange(e.target.value)}
                    />
                    <Button onClick={handleSubmit} text="hello world" styles="bg-orange-gradient ml-2" />
                </div>
            </section>
        </div>
    );
}

export default Newsletter;
