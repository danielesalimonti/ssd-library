import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {BookService} from '../../services/book.service';
import {ToastController} from "@ionic/angular";

@Component({
  selector: 'app-book',
  templateUrl: './book.page.html',
  styleUrls: ['./book.page.scss'],
})
export class BookPage implements OnInit {

  isbn: string;
  book: Book;

  constructor(private activatedRoute: ActivatedRoute,
              public router: Router,
              private auth: AuthService,
              private bookService: BookService,
              private toastController: ToastController) {

    if(!this.auth.isLogged()) {
      this.router.navigateByUrl('/login', {replaceUrl: true});
    }

    this.isbn = this.activatedRoute.snapshot.params.isbn;
  }

  ngOnInit() {
    this.bookService.showBook(this.isbn).subscribe(
      data => this.book = data,
      error => {

        if(error.status === 0){
          error.error.detail = 'Lost Connection';
        }
        localStorage.setItem('error', JSON.stringify({status: error.status, message: error.error.detail}));
        this.router.navigateByUrl('/error-page', {replaceUrl: true});
      }
    );
  }

  logout(){
    this.auth.logout().subscribe(
      data => this.router.navigateByUrl('/login', {replaceUrl: true}),
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
