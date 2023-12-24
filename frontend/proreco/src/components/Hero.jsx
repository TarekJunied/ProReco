import React from "react";
import Button from "./Button.jsx";
import { useNavigate } from "react-router-dom";
import "./styles/hero.css"; // Import the CSS file

const Hero = () => {
    const navigate = useNavigate();

    const handleClickNavigate = (page) => {
        navigate(page);
    };

    return (
        <div className="heroSection">
            <div className="box-width">
                <section id="home" className="flex md:flex-row flex-col">
                    <div className="flex-1 flex-start flex-col xl:px-0 sm:px-16 px-6 ml-36 mt-14">
                        <h1 className="hero-heading">
                            Unlock The
                        </h1>
                        <h1 className="hero-heading">
                            <span className="text-gradient">Real Power</span> {""}
                        </h1>
                        <h1 className="hero-heading">
                            Of Process
                        </h1>
                        <h1 className="hero-heading">
                            Discovery
                        </h1>
                        <p className="hero-paragraph">
                            The world&rsquo;s most sophisticated recommender
                            <br />
                            system for
                            process discovery algorithms.
                        </p>
                        <div className={`justify-between mt-10 space-x-16`}>
                            <Button text="Get started" styles="bg-dark-gradient-reversed" onClick={() => handleClickNavigate("start")} />
                            <Button text="Learn more" styles="border-4 border-orange-800" onClick={() => handleClickNavigate("processmining")} />
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Hero;
