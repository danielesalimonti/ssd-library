import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {BookService} from '../../services/book.service';
import {AlertController, ToastController} from "@ionic/angular";

@Component({
  selector: 'app-my-books',
  templateUrl: './my-books.page.html',
  styleUrls: ['./my-books.page.scss'],
})
export class MyBooksPage implements OnInit {

  loadingBooks = true;
  myBooks: Book[] = [];

  constructor(public router: Router,
              private bookService: BookService,
              private auth: AuthService,
              private toastController: ToastController) {

    if(!this.auth.isLogged()) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit() {
    this.bookService.getMyBooks().subscribe(
      (data) => {
        this.myBooks = data;
        this.loadingBooks = false;
      },
      error => {
        if(error.status === 0){
          error.error.detail = 'Lost Connection';
        }
        localStorage.setItem('error', JSON.stringify({status: error.status, message: error.error.detail}));
        this.router.navigate(['/login']);
      });
  }


  logout(){
    this.auth.logout().subscribe(
      data => this.router.navigate(['/login']),
      error => this.createToast(error)
    );
  }


  async createToast(error){
    if(error.status === 0){
      error.error.detail = 'Lost Connection';
    }

    const toast = await this.toastController.create({
      header: 'Error ',
      message: error.error.detail,
      position: 'top',
      duration: 5000,
      buttons:[
        {
          text: 'X',
          role: 'cancel'
        }
      ]
    });
    await toast.present();
  }
}
