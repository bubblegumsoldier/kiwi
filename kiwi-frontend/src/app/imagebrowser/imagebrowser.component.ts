import { Component, OnInit, HostListener  } from '@angular/core';

import { Image } from '../shared/model/Image';

import { ImageloaderService } from '../shared/imageloader/imageloader.service';

export enum KEY_CODE {
  UP_ARROW = 38,
  DOWN_ARROW = 40
}

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
    this.imageloader.getNextNImages(n).then(this.imagesLoaded.bind(this)).catch(console.error);
  }

  imagesLoaded(images :Image[])
  {
    images.forEach(this.imageLoaded.bind(this));
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
    console.log(list);
    this.images = this.images.filter((v, i) => {return i != 0});
    this.updateFeedback();
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
    console.log(this.images.length);
    if(this.images.length <= ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_THRESHOLD)
    {
      console.log("update");
      this.loadNextNImages(ImagebrowserComponent.DEFAULT_NEW_IMAGE_LOADING_NUMBER);
    }
  }

  @HostListener('window:keyup', ['$event'])
  keyEvent(event: KeyboardEvent) {
    
    if (event.keyCode === KEY_CODE.UP_ARROW) {
      this.onLike();
    }

    if (event.keyCode === KEY_CODE.DOWN_ARROW) {
      this.onDislike();
    }
  }

}
