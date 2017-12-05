import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-imagebrowser',
  templateUrl: './imagebrowser.component.html',
  styleUrls: ['./imagebrowser.component.css']
})
export class ImagebrowserComponent implements OnInit {

  private images :any[] = [];
  private likedImages :any[] = [];
  private dislikedImages :any[] = [];

  private static DEFAULT_STARTUP_IMAGE_NUMBER = 10;
  private static DEFAULT_NEW_IMAGE_LOADING_THRESHOLD = 5;

  constructor() { }

  ngOnInit()
  {
    this.images = [{
      title: "Lorem ipsum dolor sit amet",
      src: "https://www.welt.de/img/bildergalerien/mobile107274735/7572501097-ci102l-w1024/title.jpg"
    },{
      title: "Lorem ipsum dolor sit amet",
      src: "http://cdn.wonderfulengineering.com/wp-content/uploads/2014/07/129603046412160-522c.jpg"
    }];
  }

  loadNextNImages(n :number)
  {

  }

  imageLoaded(image :any)
  {
    this.images.push(image);
  }

  onDislike()
  {
    this.images[0].animateDown = true;
    setTimeout(_ => {
      this.addFirstImageToList(this.dislikedImages);
    }, 300);
  }

  onLike()
  {
    this.images[0].animateUp = true;
    console.log(this.images[0]);
    setTimeout(_ => {
      this.addFirstImageToList(this.likedImages);
    }, 300);
  }

  addFirstImageToList(list :any[])
  {
    if(this.images.length <= 0)
    {
      return;
    }
    let cImg = this.images[0];
    list.push(cImg);
    this.images = this.images.filter((v, i) => {return i != 0});
  }

  updateFeedback()
  {
    //Feedback stuff

    this.updateIfNecessary();
  }

  updateIfNecessary()
  {
    if(this.images.length <= ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_THRESHOLD)
    {
      this.loadNextNImages(ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_THRESHOLD);
    }
  }

}
