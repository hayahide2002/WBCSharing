
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django import forms
from .models import Group
from .forms import GroupForm
from django.contrib.auth.decorators import login_required
from .forms import CardSelectionForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, WellBeingCard, CardSelection

# サインアップフォーム
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

# サインアップビュー
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_unusable_password()  # パスワードを無効にする
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# ログインビュー
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            login(request, user)  # ユーザー名が存在すればログインさせる
            return redirect('home')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
    return render(request, 'login.html')

# グループ作成ビュー
@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.add(request.user)  # グループ作成者をメンバーに追加
            return redirect('home')  # ホームページにリダイレクト
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

# グループ参加ビュー
@login_required
def join_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        try:
            group = Group.objects.get(name=group_name)
            if request.user not in group.members.all():
                group.members.add(request.user)  # ユーザーをグループに追加
            return redirect('home')  # ホームページにリダイレクト
        except Group.DoesNotExist:
            return render(request, 'join_group.html', {'error': 'そのグループは存在しません'})
    return render(request, 'join_group.html')

# ホームビュー
@login_required
def home(request):
    user_groups = request.user.custom_groups.all()  # ユーザーが参加しているカスタムグループを取得
    return render(request, 'home.html', {'groups': user_groups})


@login_required
def select_cards(request, group_id):
    group = get_object_or_404(Group, id=group_id)  # グループ情報を取得
    
    # カード名と画像ファイル名を含むリストを作成
    cards = [{'name': f'Card {i}', 'image': f'card{i}.png'} for i in range(1, 31)]
    
    # 実際のデータベースからカードデータを取得
    cards = WellBeingCard.objects.all()  # WellBeingCard モデルからすべてのカードを取得

    if request.method == 'POST':
        # POSTデータの確認
        print("POST data:", request.POST)
        selected_cards = request.POST.getlist('selected_cards')
        print("Selected cards:", selected_cards)  # 選択されたカードの確認

        # ユーザーのカード選択を保存する処理
        card_selection, created = CardSelection.objects.get_or_create(user=request.user, group=group)
        card_selection.selected_cards.clear()  # 既存の選択をクリア

        # 選択されたカードを保存
        for card_name in selected_cards:
            try:
                # データベースからカードを取得して追加
                card = WellBeingCard.objects.get(name=card_name)
                card_selection.selected_cards.add(card)
                print(f"Saving card: {card.name}")
            except WellBeingCard.DoesNotExist:
                print(f"Card not found: {card_name}")

        card_selection.save()  # カード選択を保存
        return redirect('view_selections', group_id=group_id)

    # カード選択画面を表示
    return render(request, 'select_cards.html', {'group': group, 'cards': cards})


@login_required
def view_selections(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    selections = CardSelection.objects.filter(group=group)

    return render(request, 'view_selections.html', {'group': group, 'selections': selections})


