import React, { useState, useEffect } from 'react';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Button,Card, CardActionArea, CardActions, List, ListItemButton, ListItemText, ListSubheader, Collapse } from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { motion, AnimatePresence, useScroll, useSpring} from "framer-motion";
import './Home.css';



function cards(imageUrl, title, time, description,index) {
  return (
    <Card key={index}>
      <CardActionArea>
        <CardMedia component="img" height="100" image={imageUrl} alt="" padding="10px" />
        <CardContent>
          <Typography gutterBottom variant="h6" component="div">
            {title}
          </Typography>
          <Typography gutterBottom variant="h7" component="div">
            {time}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {description}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          Bring me there
        </Button>
      </CardActions>
    </Card>
  );
}


function NestedList() {
  const [open1, setOpen1] = useState(false);
  const [open2, setOpen2] = useState(false);
  const [open3, setOpen3] = useState(false);
  const [open4, setOpen4] = useState(false);
  

  const handleClick1 = () => {
    setOpen1(!open1);
  };

  const handleClick2 = () => {
    setOpen2(!open2);
  };

  const handleClick3 = () => {
    setOpen3(!open3);
  };

  const handleClick4 = () => {
    setOpen4(!open4);
  };

  return (
    <List
    sx={{ border: '1px solid #e0e0e0', borderRadius: '4px', padding: '10px' }}
      component="nav"
      aria-labelledby="nested-list-subheader"
      subheader={<ListSubheader component="div" id="nested-list-subheader"></ListSubheader>}
    >
      <ListItemButton onClick={handleClick1}>
        <ListItemText primary="Empire State Building" style={{ textAlign: 'center' }} />
        {open1 ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={open1} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ListItemButton sx={{ pl: 4 }}>
            {cards('imageUrl1', 'Title 1', 'Time 1', 'Description 1',0)}
          </ListItemButton>
        </List>
      </Collapse>

      <ListItemButton onClick={handleClick2}>
        <ListItemText primary="Wall Street" style={{ textAlign: 'center' }}/>
        {open2 ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={open2} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ListItemButton sx={{ pl: 4 }}>
            {cards('imageUrl2', 'Title 2', 'Time 2', 'Description 2',1)}
          </ListItemButton>
        </List>
      </Collapse>

      <ListItemButton onClick={handleClick3}>
        <ListItemText primary="Time Square" style={{ textAlign: 'center' }}/>
        {open3 ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={open3} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ListItemButton sx={{ pl: 4 }}>
            {cards('imageUrl3', 'Title 3', 'Time 3', 'Description 3',2)}
          </ListItemButton>
        </List>
      </Collapse>

      <ListItemButton onClick={handleClick4}>
        <ListItemText primary="Statue of Liberty"style={{ textAlign: 'center' }} />
        {open4 ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={open4} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <ListItemButton sx={{ pl: 4 }}>
            {cards('imageUrl4', 'Title 4', 'Time 4', 'Description 4',3)}
          </ListItemButton>
        </List>
      </Collapse>
    </List>
  );
}

// function HomePage() {
//   const [events, setEvents] = useState([]);
//   const [activeSlide, setActiveSlide] = useState(0);

//   useEffect(() => {
//     fetch('http://127.0.0.1:8000/api/events/')
//       .then(response => response.json())
//       .then(data => {
//         if (data.length > 0) {
//           setEvents(data.slice(0, 5)); // Only store the first 5 events
//         } else {
//           setEvents([]);
//         }
//       })
//       .catch(error => {
//         console.error(error);
//         setEvents([]);
//       });
//   }, []);

//   const handleBringMeThere = (url) => {
//     window.open(url, '_blank');
//   };

//   return (
//     <div style={{ display: 'flex', justifyContent: 'center', color: '#1C2541', fontWeight: 'bold'  }}>
//       <div>
//         <div style={{ textAlign: 'center',marginTop:'6px'}}>
//           <Carousel selectedItem={activeSlide} onChange={setActiveSlide}>
//             {events.map((event, index) => (
//                <div key={index} onMouseEnter={() => setActiveSlide(index)}>
//                 <CardActionArea>
//                   <CardMedia component="img" height="560" width="699" image={event.image} alt="image of event" padding="5px" />
//                   <CardContent>
//                     <Typography
//                     gutterBottom variant="h5"
//                     component="div"
//                     onClick={() => handleBringMeThere(event.url)}
//                     style={{ cursor: 'pointer' }}
//                      >
//                       <strong>{event.name}</strong>
//                     </Typography>
//                     <Typography variant="body2" color="#477696" >
//                       <strong>Throw in at {event.date}  {event.time}</strong>
//                     </Typography>
//                   </CardContent>
//                 </CardActionArea>
//               </div>
//             ))}
//           </Carousel>
//         </div>
//         <div style={{ marginTop: '1px' }}>
//           <NestedList />
//         </div>
//       </div>
//     </div>
//   );
// }

function HomePage() {
  const [events, setEvents] = useState([]);
  const [activeSlide, setActiveSlide] = useState(0);
  const { scrollYProgress } = useScroll();

  const scaleX = useSpring(scrollYProgress, {
    stiffness: 200,
    damping: 30,
    restDelta: 0.001
  });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/events/')
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          setEvents(data.slice(0, 5)); // Only store the first 5 events
        } else {
          setEvents([]);
        }
      })
      .catch(error => {
        console.error(error);
        setEvents([]);
      });
  }, []);

  const handleBringMeThere = (url) => {
    window.open(url, '_blank');
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', color: '#1C2541', fontWeight: 'bold' }}>
      <div>
        <div style={{ textAlign: 'center', marginTop: '6px' }}>
          <Carousel
            selectedItem={activeSlide}
            onChange={setActiveSlide}
            renderIndicator={(onClickHandler, isSelected, index) => (
              <button
                type="button"
                onClick={onClickHandler}
                style={{
                  background: isSelected ? '#1C2541' : '#ddd',
                  border: 'none',
                  borderRadius: '80%',
                  width: 10,
                  height: 10,
                  display: 'inline-block',
                  margin: '10px 10px', // Adjust the margin value as needed
                  cursor: 'pointer',
                }}
              />
            )}
          >
            {events.map((event, index) => (
              <div key={index} onMouseEnter={() => setActiveSlide(index)} onClick={() => handleBringMeThere(event.url)}>
                <CardActionArea>
                  <CardMedia component="img" height="600" width="699" image={event.image} alt="image of event"  padding="5px" marginButton="5px" />
                  <CardContent>
                    <Typography
                      gutterBottom
                      variant="h5"
                      component="div"
                      onClick={() => handleBringMeThere(event.url)}
                      style={{ cursor: 'pointer' }}
                    >
                      <strong>{event.name}</strong>  
                      <strong> {event.date} {event.time}</strong>
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </div>
            ))}
          </Carousel>
        </div>
        <div style={{ marginTop: '20px' }}>
          <NestedList />
        </div>
        <div>
          
        </div>
        
      </div>
    </div>
  );
}




export default HomePage;