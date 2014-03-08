R = importdata('user-shows.txt');

P = diag(diag(R*R'));
Q = diag(diag(R'*R));

Si = Q^(-1/2)*((R'*R)*Q^(-1/2)); % item similarity matrix 
Su = P^(-1/2)*((R*R')*P^(-1/2)); % user similairty matrix 

% Gi(u, i) is recommendation of item i for user u 
Gi = R*Si; % item-item collaborative filtering
% Gu(u, i) is recommendation of item i for user u 
Gu = Su*R; % user-user collaborative filtering

% recommendations for Alex based on user-user collaborative filtering:
Su = Gu(:, 1:100); % first hundred columns 
% the last five indices in i have the highes recommendation score 
% ru contains scores and iu contains indices; sorted in ascending 
[ru, iu] = sort(Su(500, :));
iu(90:100) % top 11 

% the same thing, except we use item-item collaborative filtering:
Si = Gi(:, 1:100);
[ri, ii] = sort(Si(500, :));
ii(90:100) % top 11

% now plot precision at top-k for various k's 
alex = importdata('alex.txt');
% plot for user-user and item-item similarity filtering 
N = 19;
xu = 1:N;
xi = 1:N;
yi = []; yu = [];
for k = 1:N
	% fraction of top-k shows watched by alex in reality 
	yu = [yu sum(alex(iu(100-k+1:100)))/k];
	yi = [yi sum(alex(ii(100-k+1:100)))/k];
end
plot(xu, yu, 'b+');
hold on;
plot(xu, yu, 'b');
plot(xi, yi, 'ro');
plot(xi, yi, 'r');
print -depsc hw2q2.eps 