g = load('graph.txt');
G = sparse(g(:,1), g(:,2), 1);

M = full(G);

for i = 1:100
	M(:,i) = M(:,i)/sum(M(:,i));
end

r = ones(100, 1)/100;

b = 0.8;

tic
for i = 1:40
	r = (1-b)*ones(100,1)/100 + b*M*r;
end
toc;
