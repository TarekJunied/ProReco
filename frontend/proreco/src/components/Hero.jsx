import styles from "../styles.js"
import Button from "./Button.jsx"

const Hero = () => {
    return (
        <div className={`${styles.flexStart} mb-10`}>
            <div className={`${styles.boxWidth}`}>
                <section id="home" className={`flex md:flex-row flex-col`}>
                    <div className={`flex-1 ${styles.flexStart} flex-col xl:px-0 sm:px-16 px-6 ml-36 mt-14`}>

                        <h1 className="font-semibold ss:text-[xr68px] text-[90px] text-white ss:leading-[100.8px] leading-85px] w-full">
                            Unlock The
                        </h1>
                        <h1 className="font-semibold ss:text-[xr68px] text-[90px] text-white ss:leading-[100.8px] leading-[80px] w-full">
                            <span className="text-gradient">Real Power</span> {""}
                        </h1>

                        <h1 className="font-semibold ss:text-[xr68px] text-[90px] text-white ss:leading-[100.8px] leading-80px] w-full m">
                            Of Process
                        </h1>
                        <h1 className="font-semibold ss:text-[xr68px] text-[90px] text-white ss:leading-[100.8px] leading-[80px] w-full">
                            Discovery
                        </h1>
                        <p className={`font-normal ss:text-[xr68px] text-[20px] text-white max-w-[470px] ${styles.paragraph}`}>
                            The world&rsquo;s most sophisticated recommender
                            <br />
                            system for
                            process discovery algorithms.
                        </p>

                        <div className={`justify-between mt-10 ${styles.flexCenter} space-x-16`}>
                            <Button text="Get started" styles="bg-dark-gradient-reversed" />
                            <Button text="Learn more" styles="border-4 border-orange-800" />

                        </div>

                    </div>


                </section >
            </div>
        </div>
    )

}

export default Hero
