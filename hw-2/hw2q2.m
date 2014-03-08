I = load('Matrix.txt');

rs = [];
ks = [197, 247, 297, 347, 397, 447, 497];
% S = S.^2;
for k = ks
	[U, S, V] = svd(I, 'econ'); % this is naive; but it works OK for small data;
	% set all except the largest k singular values to 0 
	S(k:497, k:497) = 0;
	It = U*S*V';
	Is = It*It';
	N = diag(diag(Is)); % N(i,i) = norm(di)^2
	Ics = N^(-1/2)*(Is*N^(-1/2)); % Ics(i,j) = cossim(di, dj)
	s = 0;
	for i = 1:99
		s = s+sum(Ics(i, i+1:100));
	end
	s = s/(50*99); % equivalent to s := s/binom{100}{2}
	t = 0;
	for i = 1:496
		t = t+sum(Ics(i, i+1:497));
	end
	t = t/(248*497); % equivalent to t := t/binom{497}{2}
	r = s/t;
	rs = [rs r];
end

plot(ks, rs, 'o');
hold on;
plot(ks, rs);
print -desc hw2q2.eps 