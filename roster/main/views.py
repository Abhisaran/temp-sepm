from django.http import HttpResponseRedirect
from django.shortcuts import render
from login.models import User, Staff, Manager
from django import forms


# Create your views here.
def index(request):
    print("I am here index")
    return render(request, 'main/main.html')


def logon(request, login_user, login_pass, login_mode):
    if login_mode == "manager":
        manager_list = Manager.objects.get(user_id=login_user)
        leave_history = manager_list.request_approve.split(',')
        leave_history = [x for x in leave_history if x]
        print(leave_history)
        context = {'user_string': manager_list.user_id, 'mode': "manager", 'lh': leave_history}
        return render(request, 'main/manager.html', context)
    else:
        if not User.objects.filter(user_id=login_user).exists():
            User.objects.create(user_id=login_user, password=login_pass)
            Staff.objects.create(user_id=login_user)
            staff_string = Staff.objects.get(user_id=login_user)
            staff_string.leave_allowance = staff_string.annual_leave + staff_string.carer_leave + staff_string.blood_donor_leave + staff_string.sick_certificate_leave + staff_string.sick_leave + staff_string.parental_leave + staff_string.unpaid_leave
            staff_string.save()
        # login_string_list = User.objects.get(user_id=login_user, password=login_pass)
        user_string = User.objects.get(user_id=login_user)
        staff_string = Staff.objects.get(user_id=login_user)

        leave_list = str(staff_string).split(" ")
        print(leave_list)
        leave_his = leave_list[9:]
        leave_his_string = "".join(leave_his).split(',')
        print(leave_his_string)
        leave_his_string = [x for x in leave_his_string if x]
        context = {'user_string': str(user_string.user_id), 'mode': str(login_mode),
                   'allowance': staff_string.leave_allowance, 'la': leave_list[1],
                   'al': leave_list[2], 'cl': leave_list[3], 'bdl': leave_list[4], 'scl': leave_list[5],
                   'slc': leave_list[6], 'pl': leave_list[7], 'ul': leave_list[8], 'lh': leave_his_string}

        if request.method == 'POST':
            print("LEAVE form 1")
            form = LeaveForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                print("LEAVE form 2")
                # print(form.as_p())
                # print(form.cleaned_data['leave_type'])
                # print(form.cleaned_data['leave_days'])
                return HttpResponseRedirect('/main/' + str(login_user) + '-' + str(
                    form.cleaned_data['leave_type']) + '*' + str(form.cleaned_data['leave_days']))
            else:
                print("not valid form leave")
        # if a GET (or any other method) we'll create a blank form
        else:
            form = LeaveForm()
            print("not valid form leave 2")

        context['form_leave'] = form

        return render(request, 'main/main.html', context)


def leave(request, login_user, leave_type, days):
    print("I am at leave")
    user_string = User.objects.get(user_id=login_user)
    staff_string = Staff.objects.get(user_id=login_user)
    manager_string = Manager.objects.get(user_id="abhi")
    if leave_type == "al":
        staff_string.annual_leave = staff_string.annual_leave - int(days)
    if leave_type == "cl":
        staff_string.carer_leave = staff_string.carer_leave - int(days)
    if leave_type == "bdl":
        staff_string.blood_donor_leave = staff_string.blood_donor_leave - int(days)
    if leave_type == "scl":
        staff_string.sick_certificate_leave = staff_string.sick_certificate_leave - int(days)
    if leave_type == "slc":
        staff_string.sick_leave = staff_string.sick_leave - int(days)
    if leave_type == "pl":
        staff_string.parental_leave = staff_string.parental_leave - int(days)
    if leave_type == "ul":
        staff_string.unpaid_leave = staff_string.unpaid_leave - int(days)

    staff_string.request_history = staff_string.request_history + ",[LeaveType:" + leave_type + "-Days:" + str(
        days) + "-Status:OPEN]"
    manager_string.request_approve = manager_string.request_approve + ",[Staff:" + user_string.user_id + "-LeaveType:" + leave_type + "-Days:" + str(
        days) + "-Status:OPEN]"
    staff_string.save()
    manager_string.save()
    return HttpResponseRedirect(
        '/main/' + str(user_string.user_id) + '-' + str(user_string.password) + '-' + str("staff"))


def leave_status_manager(request, string):
    typeOfReq = str(string).split(']')
    if str(string).find("Status") == -1:
        return HttpResponseRedirect('/login/')
    whois = ""
    if typeOfReq[1] == "Accept":
        temp_string = str(typeOfReq[0]).replace('[', '').replace('\'', '').split('-')
        staff_user_id = temp_string[0].replace("Staff:", '')
        leave_type = temp_string[1].replace("LeaveType:", '')
        number_days = temp_string[2].replace("Days:", '')
        status = temp_string[3].replace("Status:", '')

        staff_string = Staff.objects.get(user_id=staff_user_id)
        leave_his = staff_string.request_history
        manager_string = Manager.objects.get(user_id="abhi")
        manager_leave_his = manager_string.request_approve
        new_leave_his = leave_his.replace(
            "[LeaveType:" + leave_type + "-Days:" + str(number_days) + "-Status:" + status + "]",
            "[LeaveType:" + leave_type + "-Days:" + str(number_days) + "-Status:" + "ACCEPTED" + "]")
        staff_string.request_history = new_leave_his
        new_manager_his = manager_leave_his.replace(
            "Staff:" + staff_user_id + "-LeaveType:" + leave_type + "-Days:" + str(
                number_days) + "-Status:" + status + "]",
            "Staff:" + staff_user_id + "-LeaveType:" + leave_type + "-Days:" + str(
                number_days) + "-Status:" + "ACCEPTED" + "]")
        manager_string.request_approve = new_manager_his
        staff_string.save()
        manager_string.save()
        whois = "abhi-abhi-manager"
        return HttpResponseRedirect('/main/' + whois)


    if typeOfReq[1] == "Reject":
        temp_string = str(typeOfReq[0]).replace('[', '').replace('\'', '').split('-')
        staff_user_id = temp_string[0].replace("Staff:", '')
        leave_type = temp_string[1].replace("LeaveType:", '')
        number_days = temp_string[2].replace("Days:", '')
        status = temp_string[3].replace("Status:", '')

        staff_string = Staff.objects.get(user_id=staff_user_id)
        leave_his = staff_string.request_history
        manager_string = Manager.objects.get(user_id="abhi")
        manager_leave_his = manager_string.request_approve
        new_leave_his = leave_his.replace(
            "[LeaveType:" + leave_type + "-Days:" + str(number_days) + "-Status:" + status + "]",
            "[LeaveType:" + leave_type + "-Days:" + str(number_days) + "-Status:" + "REJECTED" + "]")
        staff_string.request_history = new_leave_his
        new_manager_his = manager_leave_his.replace(
            "Staff:" + staff_user_id + "-LeaveType:" + leave_type + "-Days:" + str(
                number_days) + "-Status:" + status + "]",
            "Staff:" + staff_user_id + "-LeaveType:" + leave_type + "-Days:" + str(
                number_days) + "-Status:" + "REJECTED" + "]")
        manager_string.request_approve = new_manager_his
        staff_string.save()
        manager_string.save()
        whois = "abhi-abhi-manager"
        return HttpResponseRedirect('/main/' + whois)


    if typeOfReq[1].find("Close") != -1:
        temp_string = str(typeOfReq[0]).replace('[', '').replace('\'', '').split('-')
        staff_user_id = typeOfReq[1].split("*")[0]
        # staff_user_id = temp_string[0].replace("Staff:", '')
        leave_type = temp_string[0].replace("LeaveType:", '')
        number_days = temp_string[1].replace("Days:", '')
        status = temp_string[2].replace("Status:", '')

        staff_string = Staff.objects.get(user_id=staff_user_id)
        leave_his = staff_string.request_history
        manager_string = Manager.objects.get(user_id="abhi")
        manager_leave_his = manager_string.request_approve
        new_leave_his = leave_his.replace(
            "[LeaveType:" + leave_type + "-Days:" + str(number_days) + "-Status:" + status + "]",
            "[LeaveType:" + leave_type + "-Days:" + str(number_days) + "-Status:" + "CLOSED" + "]")
        staff_string.request_history = new_leave_his
        new_manager_his = manager_leave_his.replace(
            "Staff:" + staff_user_id + "-LeaveType:" + leave_type + "-Days:" + str(
                number_days) + "-Status:" + status + "]",
            "Staff:" + staff_user_id + "-LeaveType:" + leave_type + "-Days:" + str(
                number_days) + "-Status:" + "CLOSED" + "]")
        manager_string.request_approve = new_manager_his
        staff_string.save()
        manager_string.save()
        whois = staff_user_id + '-' + staff_user_id + "-staff"
        return HttpResponseRedirect('/main/' + whois)
    else:
        return HttpResponseRedirect('/login/')


class LeaveForm(forms.Form):
    leave_choice = [('al', 'Annual Leave'), ('cl', 'Carer Leave'), ('bdl', 'Blood Donor Leave'),
                    ('scl', 'Sick Certificate Leave'), ('slc', 'Sick Leave Without Certificate'),
                    ('pl', 'Paid Leave'), ('ul', 'Unpaid Leave')]
    leave_type = forms.ChoiceField(label='', choices=leave_choice,
                                   widget=forms.Select(attrs={'class': 'field'}))
    leave_days = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'No of Days'}))
