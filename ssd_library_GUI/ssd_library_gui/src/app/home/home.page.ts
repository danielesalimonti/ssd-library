import {Component, OnInit} from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {BookService} from '../../services/book.service';
import {AuthService} from '../../services/auth.service';
import {ToastController} from "@ionic/angular";

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  loadingBooks = true;
  loadingMyBooks = true;
  books: Book[] = [];
  isMyBook: string[] = [];

  constructor(private router: Router,
              private bookService: BookService,
              private auth: AuthService,
              private toastController: ToastController) {

    if(!this.auth.isLogged()) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit() {
    this.bookService.getAllBooks().subscribe(
      (data) => {
        this.books = data;
        this.loadingBooks = false;

        this.updateButtons();
      },
      error => {
        if(error.status === 0){
          error.error.detail = 'Lost Connection';
        }
        localStorage.setItem('error', JSON.stringify({status: error.status, message: error.error.detail}));
        this.router.navigate(['/login']);
      });
  }

  updateButtons(){
    this.bookService.getMyBooks().subscribe(
      (myBooks) => {
        this.isMyBook = [];
        myBooks.forEach( (b) => {
          this.isMyBook.push(b.ISBN);
        });
        this.loadingMyBooks = false;
      },
      error => this.createToast(error));
  }

  rent(isbn){
    this.bookService.rentBook(isbn).subscribe(
      data => {
        this.isMyBook.push(isbn);
        this.router.navigate(['/book/',isbn]);
        },
      error => this.createToast(error)
    );
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
