from flask import flash, render_template, request, redirect, url_for, session
from models import db as db, User_entry, Influencer, Sponsor, Campaign,CampaignRequest
from app import app
import logging
from sqlalchemy.exc import OperationalError, IntegrityError
from datetime import datetime




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/influencer_register')
def influencer_register():
    return render_template('influencer_register.html')


@app.route('/sponsor_register')
def sponsor_register():
    return render_template('sponsor_register.html')


@app.route('/submit_influencer_registration', methods=['POST'])
def submit_influencer_registration():
    username = request.form['username']
    email = request.form['email']
    niche = request.form['niche']
    platform = request.form['platform']
    followers = request.form['followers']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if not username or not email or not niche or not platform or not followers or not password or not confirm_password:
        return "Please fill out all the details"
   
    if password != confirm_password:
        return "Passwords do not match!", 400


   
    influencer = Influencer(username=username, email=email, niche=niche, platform=platform, followers=followers, password=password)
    try:
        db.session.add(influencer)
        db.session.commit()
        logging.info(f"Successfully registered influencer: {influencer.username}")
       
        try:
            id=str(influencer.id)+"_influencer"
            user_entry = User_entry(id=id, username=username, password=password, role='influencer')
            # Write to UserEntry table after successful write to Influencer
            db.session.add(user_entry)
            db.session.commit()
            logging.info(f"Successfully added to user_entry: {user_entry.username}")
            return redirect(url_for('index'))
       
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError while writing to user_entry: {e.orig}")
            return f"IntegrityError in user_entry: {e.orig}", 400
       
        except OperationalError as e:
            db.session.rollback()
            logging.error(f"OperationalError while writing to user_entry: {e.orig}")
            return f"OperationalError in user_entry: {e.orig}", 500
       
        except Exception as e:
            db.session.rollback()
            logging.error(f"An error occurred while writing to user_entry: {str(e)}")
            return f"An error occurred in user_entry: {str(e)}", 500
   
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"IntegrityError: {e.orig}")
        return f"IntegrityError: {e.orig}", 400
   
    except OperationalError as e:
        db.session.rollback()
        logging.error(f"OperationalError: {e.orig}")
        return f"OperationalError: {e.orig}", 500
   
    except Exception as e:
        db.session.rollback()
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}", 500


    return redirect(url_for('index'))


@app.route('/submit_sponsor_registration', methods=['POST'])
def submit_sponsor_registration():
    username = request.form['username']
    email = request.form['email']
    industry = request.form['industry']
    password = request.form['password']
    confirm_password = request.form['confirm_password']


    if password != confirm_password:
        return "Passwords do not match!", 400


    sponsor = Sponsor(company_name=username, industry=industry, budget=0, email=email, password=password)
   
    try:
        db.session.add(sponsor)
        db.session.commit()
        logging.info(f"Successfully registered sponsor: {sponsor.company_name}")
       
        try:
            id=str(sponsor.id)+"_sponsor"
            user_entry = User_entry(id=id, username=username, password=password, role='sponsor')
            # Write to UserEntry table after successful write to Influencer
            db.session.add(user_entry)
            db.session.commit()
            logging.info(f"Successfully added to user_entry: {user_entry.username}")
            return redirect(url_for('index'))
       
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError while writing to user_entry: {e.orig}")
            return f"IntegrityError in user_entry: {e.orig}", 400
       
        except OperationalError as e:
            db.session.rollback()
            logging.error(f"OperationalError while writing to user_entry: {e.orig}")
            return f"OperationalError in user_entry: {e.orig}", 500
       
        except Exception as e:
            db.session.rollback()
            logging.error(f"An error occurred while writing to user_entry: {str(e)}")
            return f"An error occurred in user_entry: {str(e)}", 500
   
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"IntegrityError: {e.orig}")
        return f"IntegrityError: {e.orig}", 400
   
    except OperationalError as e:
        db.session.rollback()
        logging.error(f"OperationalError: {e.orig}")
        return f"OperationalError: {e.orig}", 500
   
    except Exception as e:
        db.session.rollback()
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}", 500


    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']


    user = User_entry.query.filter_by(username=username).first()
    if user and user.password == password:  # Directly compare plain text passwords
        session['user_id'] = user.id
        session['role'] = user.role
        if user.role == 'influencer':
            return redirect(url_for('influencer_dashboard'))
        elif user.role == 'sponsor':
            return redirect(url_for('sponsor_dashboard'))
        elif user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
    else:
        return "Invalid credentials!", 400






@app.route('/influencer_dashboard')
def influencer_dashboard():
    if 'user_id' not in session or session['role'] != 'influencer':
        return redirect(url_for('index'))
    user = Influencer.query.get(session['user_id'].split('_')[0])
    # Get the active campaigns
    today = datetime.utcnow().date()
    active_campaigns = Campaign.query.filter(Campaign.status == True, Campaign.end_date > today).all()
    taken_campaigns = CampaignRequest.query.filter(CampaignRequest.influencer_id == session['user_id']).all()
    return render_template('influencer_dashboard.html', user=user, active_campaigns=active_campaigns,taken_campaigns=taken_campaigns)


    #return render_template('influencer_dashboard.html', user=user)


@app.route('/sponsor_dashboard')
def sponsor_dashboard():
    if 'user_id' not in session or session['role'] != 'sponsor':
        return redirect(url_for('index'))
    spon_user = Sponsor.query.get(session['user_id'].split('_')[0])
    sponsor_id = session['user_id']
    # Query all campaigns for the logged-in sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()


    return render_template('sponsor_dashboard.html', spon_user=spon_user,campaigns=campaigns)




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('index'))




@app.route('/create_campaign', methods=['POST'])
def create_campaign():
    name = request.form['name']
    description = request.form['description']
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    budget = request.form['budget']
    visibility = request.form['visibility']
    goals = request.form['goals']


    # Convert the start_date and end_date from string to datetime object
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    #session['user_id']
    #    session['role']
    new_campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility,
        goals=goals,
        sponsor_id=session['user_id'],
        status=True
    )


    db.session.add(new_campaign)
    db.session.commit()


    return redirect(url_for('sponsor_dashboard'))


@app.route('/activate_campaign/<int:campaign_id>', methods=['POST'])
def activate_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.status = True
        db.session.commit()
    return redirect(url_for('sponsor_dashboard'))


@app.route('/deactivate_campaign/<int:campaign_id>', methods=['POST'])
def deactivate_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.status = False
        db.session.commit()
    return redirect(url_for('sponsor_dashboard'))


@app.route('/respond_campaign/<int:campaign_id>', methods=['POST'])
def respond_campaign(campaign_id):
    response = request.form.get('response')
    influencer_id = session['user_id']# Implement this function based on your auth system
    campaign = Campaign.query.get_or_404(campaign_id)
    sponsor_id=campaign.sponsor_id
    #influencer_campaign = InfluencerCampaign.query.filter_by(campaign_id=campaign_id, influencer_id=influencer_id).first()
    date_of_request = datetime.now().date()
    date_of_modification = datetime.now().date()


    if response == 'accept':
        status='accept'
        #flash('Campaign accepted!')
    elif response == 'reject':
        status='reject'
        #flash('Campaign rejected!')
    else:
        flash('Invalid response!')


    new_campaign_req = CampaignRequest(
        campaign_id=campaign_id,
        sponsor_id=sponsor_id,
        influencer_id=influencer_id,
        date_of_request=date_of_request,
        date_of_modification=date_of_modification,
        status=status
    )


    db.session.add(new_campaign_req)
    db.session.commit()


    db.session.commit()
    return redirect(url_for('influencer_dashboard'))


@app.route('/edit_campaign/<int:campaign_id>', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
   
    if request.method == 'POST':
        # Update the campaign details
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        campaign.budget = request.form['budget']
        campaign.visibility = request.form['visibility']
        campaign.goals = request.form['goals']
       
        try:
            db.session.commit()
            flash('Campaign updated successfully!')
            return redirect(url_for('sponsor_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating campaign: {str(e)}', 'danger')
            return redirect(url_for('edit_campaign', campaign_id=campaign_id))
   
    return render_template('edit_campaign.html', campaign=campaign)


@app.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
   
    try:
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting campaign: {str(e)}', 'danger')
   
    return redirect(url_for('sponsor_dashboard'))










@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
   
    active_influencers = Influencer.query.count()
    active_sponsors = Sponsor.query.count()
    total_campaigns = Campaign.query.count()
    public_campaigns = Campaign.query.filter_by(visibility='public').count()
    private_campaigns = Campaign.query.filter_by(visibility='private').count()
    pending_requests = CampaignRequest.query.filter_by(status='pending').count()
    accepted_requests = CampaignRequest.query.filter_by(status='accept').count()
    rejected_requests = CampaignRequest.query.filter_by(status='reject').count()
    flagged_influencers = 0
    flagged_sponsors = 0


    return render_template('admin_dashboard.html',
                           active_influencers=active_influencers,
                           active_sponsors=active_sponsors,
                           total_campaigns=total_campaigns,
                           public_campaigns=public_campaigns,
                           private_campaigns=private_campaigns,
                           pending_requests=pending_requests,
                           accepted_requests=accepted_requests,
                           rejected_requests=rejected_requests,
                           flagged_influencers=flagged_influencers,
                           flagged_sponsors=flagged_sponsors)



@app.route('/find', methods=['GET'])
def find():
    influencers = Influencer.query.all()
    campaigns = Campaign.query.filter_by(status=1).all()
    sponsors = Sponsor.query.all()
    print(campaigns)
    return render_template('find.html', influencers=influencers, campaigns=campaigns, sponsors=sponsors)

@app.route('/search_influencers', methods=['POST'])
def search_influencers():
    influencer_id = request.form.get('influencer')
    selected_influencer = Influencer.query.get(influencer_id)
    # Process the selected influencer
    return render_template('search_results.html', influencer=selected_influencer)

@app.route('/search_campaigns', methods=['POST'])
def search_campaigns():
    campaign_id = request.form.get('campaign')
    selected_campaign = Campaign.query.get(campaign_id)
    # Process the selected campaign
    return render_template('search_results.html', campaign=selected_campaign)

@app.route('/search_sponsors', methods=['POST'])
def search_sponsors():
    sponsor_id = request.form.get('sponsor')
    selected_sponsor = Sponsor.query.get(sponsor_id)
    # Process the selected sponsor
    return render_template('search_results.html', sponsor=selected_sponsor)
