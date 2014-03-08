%
% NOTE: When searching for top k NNs, we pass k+1 to lshlookup, because the top 1st NN is the query point itself; see the provided source code for details 
% 
% Blaz Sovdat, MMDS class, 2014. 
%

%% First item for part (d) of HWQ4
L = 10;
k = 24;

T1 = lsh('lsh', L, k, size(patches, 1), patches, 'range', 255);

avg_lsh_tm = 0.0;
avg_lin_tm = 0.0;
err = 0.0; 
for i = 100:100:1000
	tic;
	% Finds top 3 NNs of i-th image under L1 norm 
	[nnlsh, numcand] = lshlookup(patches(:, i), patches, T1, 'k', 4, 'distfun', 'lpnorm', 'distargs', {1});
	if length(nnlsh) < 3
		fprintf('Yikes\n') 
	end
	avg_lsh_tm = avg_lsh_tm+toc;
	tic;
	nnlin = linear_search(patches, i, 4);
	avg_lin_tm = avg_lin_tm+toc;
	
	d_lin = norm(patches(:, i)-patches(:, nnlin(2)), 1)+norm(patches(:, i)-patches(:, nnlin(3)), 1)+norm(patches(:, i)-patches(:, nnlin(4)), 1);
	d_lsh = norm(patches(:, i)-patches(:, nnlsh(2)), 1)+norm(patches(:, i)-patches(:, nnlsh(3)), 1)+norm(patches(:, i)-patches(:, nnlsh(4)), 1);
	err = err+d_lsh/d_lin;
end

avg_lsh_tm = avg_lsh_tm/10
avg_lin_tm = avg_lin_tm/10
err = err/10

% Show the 3 NN
%figure(2); clf;
%for k = 1:4
%	subplot(2, 5, k);
%	imagesc(reshape(patches(:, nnlsh(k+1)), 20, 20));
%	colormap gray;
%	axis image;
%end
