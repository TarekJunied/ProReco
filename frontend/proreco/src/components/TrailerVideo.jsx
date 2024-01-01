import React from 'react'
import ReactPlayer from 'react-player';

const demoUrl = "https://youtu.be/ULLoRT4Vyn4"
const labelStyle = {
  color: "white",
  fontWeight: 500,
  fontSize: "5vw",
  marginBottom: "2vh"

}

const TrailerVideo = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: "100%",
        height: "100%"
      }}
    >
      <h1 style={labelStyle}>A demo of ProReco</h1>
      <ReactPlayer
        url={demoUrl}
        width='100%'
        height='100%'
        playing={false}
      ></ReactPlayer>
    </div>
  )
}

export default TrailerVideo
