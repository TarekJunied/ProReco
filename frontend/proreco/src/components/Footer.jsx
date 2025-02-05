
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import styles from "../styles";
import Logo from './Logo';
import { footerLinks, socialMedia } from "../constants";

const Footer = () => {
    const navigate = useNavigate();

    const handleNavigateLink = (link) => {
        if (link.name == "Contribute") {
            window.open(link.link)
        }
        else {
            navigate(link.link)
        }
    }

    return (

        <section className={`${styles.flexCenter} ${styles.paddingY} flex-col`}>
            <div className={`${styles.flexStart} md:flex-row flex-col mb-8 w-full`}>
                <div className="flex-[1] flex flex-col justify-start mr-10">
                    <div style={{ display: 'flex', alignItems: 'center', height: "8vh", marginTop: "0.5vh", marginLeft: "3.5vw" }}>
                        <Logo />
                    </div>
                    <p className={`${styles.paragraph} ml-4 mt-4 max-w-[312px]`}>
                        Unlock the real power of process discovery.
                    </p>
                </div>

                <div className="flex-[1.5] w-full flex flex-row justify-between flex-wrap md:mt-0 mt-10">
                    {footerLinks.map((footerlink) => (
                        <div key={footerlink.title} className={`flex flex-col ss:my-0 my-4 min-w-[150px]`}>

                            <ul className="list-none mt-4">
                                {footerlink.links.map((link, index) => (
                                    <li
                                        key={link.name}
                                        className={`font-normal text-[16px] leading-[24px] text-white hover:text-secondary cursor-pointer ${index !== footerlink.links.length - 1 ? "mb-4" : "mb-0"}`}
                                        onClick={() => handleNavigateLink(link)}
                                    >
                                        {link.name}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            </div>

            <div className="w-full flex justify-between items-center md:flex-row flex-col pt-6 border-t-[1px] border-t-[#3F3E45]">
                <p className="font-poppins font-normal text-center text-[18px] leading-[27px] text-white ml-4">
                    Copyright Ⓒ 2023 ProReco. All Rights Reserved.
                </p>

                <div className="flex flex-row md:mt-0 mt-6 mr-4">
                    {socialMedia.map((social, index) => (
                        <img
                            key={social.id}
                            src={social.icon}
                            alt={social.id}
                            className={`w-[21px] h-[21px] object-contain cursor-pointer ${index !== socialMedia.length - 1 ? "mr-6" : "mr-0"
                                }`}
                            style={{ color: "white" }}
                            onClick={() => window.open(social.link)}
                        />
                    ))}
                </div>
            </div>
        </section>

    );
};

export default Footer;