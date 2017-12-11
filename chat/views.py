from django.views import generic
from braces.views import LoginRequiredMixin

from core.models import Valuation

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from . import models
from . import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q


class DialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat/dialogs.html'
    model = models.Dialog
    ordering = 'modified'

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user)).order_by('-modified')
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('id'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), id=self.kwargs.get('id'))
            dialog = utils.get_dialogs_with_user(self.request.user, user)
            if self.request.user != user and user.is_superuser is False:
                if len(dialog) == 0:
                    dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
                else:
                    dialog = dialog[0]

                context['active_dialog'] = dialog
                context['my_value'] = True
            else:
                if self.object_list:
                    context['active_dialog'] = self.object_list[0]
                    context['my_value'] = True
                else:
                    context['my_value'] = False
        else:
            if self.object_list:
                context['active_dialog'] = self.object_list[0]
                context['my_value'] = True
            else:
                context['my_value'] = False

        if context['my_value']:
            if self.request.user == context['active_dialog'].owner:
                context['opponent_username'] = context['active_dialog'].opponent.username
                context['myOpponent'] = Valuation.objects.filter(user=self.object_list[0].opponent.id).last()

            else:
                context['opponent_username'] = context['active_dialog'].owner.username
                context['myOpponent'] = Valuation.objects.filter(user=self.object_list[0].owner.id).last()
        else:
            pass
        return context


