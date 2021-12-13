import { Component, OnInit } from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {BookService} from '../../services/book.service';
import {AlertController, ToastController} from "@ionic/angular";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-my-books',
  templateUrl: './my-books.page.html',
  styleUrls: ['./my-books.page.scss'],
})
export class MyBooksPage implements OnInit {

  loadingBooks = true;
  myBooks: Book[] = [];
  searchField: FormControl = new FormControl('');
  orderField: FormControl = new FormControl('');

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


  filter(books: Book[]): Book[]{
    return books.filter(b => this.searchField.value === ''
      || b.ISBN.includes(this.searchField.value)
      || b.title.toLowerCase().includes(this.searchField.value.toLowerCase())
      || b.author.toLowerCase().includes(this.searchField.value.toLowerCase()));
  }

  sort(books: Book[]): Book[]{
    return books.sort( (a, b) => {
      switch(this.orderField.value){
        case 'ISBN': return a.ISBN > b.ISBN ? 1 : 0;
        case 'Title': return a.title > b.title ? 1 : 0;
        case 'Author': return a.author > b.author ? 1 : 0;
        case 'PublishDate': return a.published_date > b.published_date ? 1 : 0;
        default: return 0;
      }});
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
