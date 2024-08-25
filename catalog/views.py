from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, VersionFormset
from catalog.models import Product, Version


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-контроллер для добавления нового абонемента.
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        """
        Формирует опцию для указания версии абонемента при его добавлении.
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        """
        Автоматически привязывает пользователя к продукту (абонементу).
        """
        product = form.save()
        product.user = self.request.user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс-контроллер для внесения изменений в абонемент.
    """
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        """
        Переходит к странице измененного абонемента.
        """
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """
        Формирует опцию для указания новой версии абонемента при внесении изменений в него.
        """
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, formset=VersionFormset, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_form_class(self):
        """
        Проверяет права доступа пользователя на внесение изменений в продукт (абонемент).
        """
        user = self.request.user
        if user == self.object.user:
            return ProductForm
        if user.has_perm("catalog.can_cancel_publication") and user.has_perm(
                "catalog.can_change_description") and user.has_perm("catalog.can_change_category"):
            return ProductForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-контроллер для удаления абонемента.
    """
    model = Product
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        """
        Проверяет права доступа на удаление продукта (абонемента).
        """
        product = Product.objects.get(pk=self.kwargs['pk'])
        return self.request.user.is_superuser or self.request.user.pk == product.user.pk


class ProductListView(ListView):
    """
    Класс-контроллер для выведения страницы со списком абонементов (главная, home).
    """
    model = Product


class InstructorView(TemplateView):
    """
    Класс-контроллер для выведения страницы со списком тренеров (instructor).
    """
    template_name = 'catalog/instructor.html'


class ProductDetailView(DetailView):
    """
    Класс-контроллер для выведения страницы абонемента с подробностями.
    """
    model = Product


class ContactView(TemplateView):
    """
    Класс-контроллер для выведения страницы с контактами (contact).
    """
    template_name = 'catalog/contact.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Создает форму для обратной связи.
        """
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f"You have new message from {name} ({phone}): {message}")
        return render(request, "catalog/contact.html")
