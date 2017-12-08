import { Component, OnInit } from '@angular/core';

import { Image } from '../shared/model/Image';

import { ImageloaderService } from '../shared/imageloader/imageloader.service';

@Component({
  selector: 'app-imagebrowser',
  templateUrl: './imagebrowser.component.html',
  styleUrls: ['./imagebrowser.component.css']
})
export class ImagebrowserComponent implements OnInit {

  private images :Image[] = [];
  private likedImages :Image[] = [];
  private dislikedImages :Image[] = [];

  private static DEFAULT_STARTUP_IMAGE_NUMBER = 10;
  private static DEFAULT_NEW_IMAGE_LOADING_THRESHOLD = 5;
  private static DEFAULT_NEW_IMAGE_LOADING_NUMBER = 5;

  constructor(private imageloader :ImageloaderService)
  {

  }

  ngOnInit()
  {
    this.loadNextNImages(ImagebrowserComponent.DEFAULT_STARTUP_IMAGE_NUMBER);
  }

  loadNextNImages(n :number)
  {
    this.imageloader.getNextNImages(n).then(this.imagesLoaded).then(alert);
  }

  imagesLoaded(images :Image[])
  {
    this.images.forEach(this.imageLoaded);
  }

  imageLoaded(image :Image)
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

  //TODO: This method is too long
  updateFeedback()
  {
    let likeFeedbackRequests :Promise<void>[] = this.likedImages.map(image => {
      return this.imageloader.sendFeedback(image.id, true);
    });
    let dislikeFeedbackRequests :Promise<void>[] = this.dislikedImages.map(image => {
      return this.imageloader.sendFeedback(image.id, false);
    });
    let likedImagesSafetyCopy = this.likedImages.slice();
    let dislikedImagesSafetyCopy = this.dislikedImages.slice();

    this.likedImages = [];
    this.dislikedImages = [];
    
    let allRequests = likeFeedbackRequests.concat(dislikeFeedbackRequests);
    Promise.all(allRequests).then(_ => {
      console.log("All feedbacks were sent (" + allRequests.length + ")");
    }).catch(error => {
      console.error(error);
      this.likedImages = this.likedImages.concat(likedImagesSafetyCopy);
      this.dislikedImages = this.dislikedImages.concat(dislikedImagesSafetyCopy);
    });

    this.updateIfNecessary();
  }

  updateIfNecessary()
  {
    if(this.images.length <= ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_THRESHOLD)
    {
      this.loadNextNImages(ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_NUMBER);
    }
  }

}
